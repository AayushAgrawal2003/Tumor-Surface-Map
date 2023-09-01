#! /usr/bin/env python


import cv2
import numpy as np  
import struct

import tf2_ros
import tf2_geometry_msgs

from geometry_msgs.msg import Pose
import rospy
blue = struct.unpack('I', struct.pack('BBBB', 255, 0, 0, 255))[0]
green = struct.unpack('I', struct.pack('BBBB', 0 ,255, 0, 255))[0]


END_TO_PROBE = 40
DIAMETER = 20
PC_DENSITY = 10


# Get the values of the tumor location
def vals(main):
    cimg = cv2.cvtColor(main,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(main,cv2.HOUGH_GRADIENT,1,20,
    param1=80,param2=50,minRadius=20,maxRadius=60)  
    if circles is None:
        return 0,0 
    circles = np.uint16(np.around(circles))
    cols,rows= main.shape 
    for i in circles[0,:]:
        # draw the outer circle
        # TODO: Convert pixels to cm    
        scale =  DIAMETER / (1000 * (i[2] /2)) 
        x,y = scale* (cols //2 - i[0]), scale * (i[1] + END_TO_PROBE)
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle

        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        # cv2.imshow('detected circles' + str(i),cimg) 


    # Assuming x to be the x displacement in the frame of the robotic arm 
    # Assuming y to be the z displacement
    
    return x,y



def transform_pose(input_pose, from_frame, to_frame , tf_buffer):

    # **Assuming /tf2 topic is being broadcasted

    pose_stamped = tf2_geometry_msgs.PoseStamped()
    pose_stamped.pose = input_pose
    pose_stamped.header.frame_id = from_frame
    pose_stamped.header.stamp =  rospy.Time()

    try:
        # ** It is important to wait for the listener to start listening. Hence the rospy.Duration(1)
        output_pose_stamped = tf_buffer.transform(pose_stamped, to_frame, rospy.Duration(10))
        return [output_pose_stamped.pose.position.x , output_pose_stamped.pose.position.y, output_pose_stamped.pose.position.z, green]

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        raise


def transform_pc(points, from_frame, to_frame):
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)

    tf_points = []
    for point in points:
        new = Pose()
        new.position.x = point[0]
        new.position.y = point[1]
        new.position.z = point[2]
        new.orientation.x = 0.0
        new.orientation.y = 0.0
        new.orientation.z = 0.0
        new.orientation.w = 1.0
        tf_points.append(transform_pose(new,from_frame ,to_frame, tf_buffer))


    return tf_points




def sphere(x,y,z):
    r = DIAMETER / 2000

    points = []
    for j in range(-90,90 ,PC_DENSITY):
        k = 0
        points.append([x + r * np.cos(k) * np.cos(j) , y + r * np.sin(k) * np.cos(j) , z + r * np.sin(j) , blue])


    return points