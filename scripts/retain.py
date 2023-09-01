#! /usr/bin/env python

import rospy
from visualization_msgs.msg import Marker , MarkerArray
import cv2 as cv

from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError
rospy.init_node('rviz_marker')
import tf2_ros
import tf2_geometry_msgs
import rospy

from utils import vals , transform_pose


class process():
    def __init__(self):
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
        self.markerArray_pub = rospy.Publisher("/visualization_markerArray", MarkerArray, queue_size = 2)
        self.br = CvBridge()
        self.marker = Marker()
        self.temp = Marker()
        self.markerArray = MarkerArray()
        self.marker.header.frame_id = "iiwa_link_7"
        # self.marker.header.stamp = rospy.Time.now()

        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        self.marker.type = 2
        self.marker.id = 0

        # Set the scale of the self.marker
        self.marker.scale.x = 0.05
        self.marker.scale.y = 0.05
        self.marker.scale.z = 0.05

        # Set the color
        self.marker.color.r = 0.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
        self.marker.color.a = 1.0

        # Set the pose of the self.marker
        self.marker.pose.position.x = 0
        self.marker.pose.position.y = 0
        self.marker.pose.position.z = 0
        self.marker.pose.orientation.x = 0.0
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = 1.0


        # Temp Value

        self.temp.header.frame_id = "world"
        # self.marker.header.stamp = rospy.Time.now()

        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        self.temp.type = 2
        self.temp.id = 0

        self.temp.color.r = 0.0
        self.temp.color.g = 1.0
        self.temp.color.b = 0.0
        self.temp.color.a = 1.0

        self.temp.scale.x = 0.05
        self.temp.scale.y = 0.05
        self.temp.scale.z = 0.05

    def process_image(self, data):
        cv2_img = self.br.imgmsg_to_cv2(data)
        self.marker.pose.position.x, self.marker.pose.position.z = vals(cv2_img)
        self.temp.pose = transform_pose(self.marker.pose, "iiwa_link_7" , "world")
        if self.markerArray.markers:
            if self.markerArray.markers[-1] != self.temp:
                self.markerArray.markers.append(self.temp)
        else:
            self.markerArray.markers.append(self.temp)

        
        # print(len(self.markerArray.markers))

        # self.markerArray.markers.append(self.marker)

    def run(self):
        # Change to the published us image in real time
        rospy.Subscriber("/us_image", Image, self.process_image)
        self.marker_pub.publish(self.marker)
        self.markerArray_pub.publish(self.markerArray)



new = process()

while not rospy.is_shutdown():
  new.run()
  rospy.rostime.wallsleep(0.01)
