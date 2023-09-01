#! /usr/bin/env python

import rospy

import cv2 as cv
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError
rospy.init_node('rviz_marker')

from utils import vals ,sphere, transform_pc



from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header




class process():
    def __init__(self):
        self.global_point_holder = []
        self.marker_pub = rospy.Publisher("/point_cloud", PointCloud2, queue_size = 2)
        self.world_pc = rospy.Publisher("/point_cloud_world", PointCloud2, queue_size = 2)
        self.br = CvBridge()
        self.fields = [PointField('x', 0, PointField.FLOAT32, 1),
                PointField('y', 4, PointField.FLOAT32, 1),
                PointField('z', 8, PointField.FLOAT32, 1),
                # PointField('rgb', 12, PointField.UINT32, 1),
                PointField('rgba', 12, PointField.UINT32, 1),
                ]

    def process_image(self, data):
        cv2_img = self.br.imgmsg_to_cv2(data)
        x , z = vals(cv2_img)
        # print(x,z)
        if x == 0 and z == 0:
            points = []
        else:
            points = sphere(x,0,z)


        world_points = transform_pc(points,"iiwa_link_ee" ,"world")
        self.global_point_holder += world_points
        header = Header()
        header.frame_id = "iiwa_link_ee"
        header.stamp =  rospy.Time(0)

        self.pc2 = point_cloud2.create_cloud(header, self.fields, points)

        self.marker_pub.publish(self.pc2)


        header = Header()
        header.frame_id = "world"
        header.stamp =  rospy.Time(0)

        if world_points is not None:
            self.pc2_world = point_cloud2.create_cloud(header, self.fields, self.global_point_holder)
            # print(self.pc2)
            self.world_pc.publish(self.pc2_world)


         

    def run(self):
        # Change to the published us image in real time
        rospy.Subscriber("/us_image", Image, self.process_image)
        rospy.spin()


new = process()

while not rospy.is_shutdown():
  new.run()
  rospy.rostime.wallsleep(0.001)
