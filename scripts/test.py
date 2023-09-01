#! /usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
import cv2 
import glob
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError
import time

rospy.init_node('test_pub')

br = CvBridge()

pub = rospy.Publisher("/us_image" , Image, queue_size=10)

img_arr = []
for img in glob.glob("/home/inspire_01/catkin_ws/src/us_volume/dummy_images/*.jpg"):
    img_arr.append(img)

itr = 0
init = time.time()

while not rospy.is_shutdown():
    # Change 0 to itr if you want to iterate over values
    n= cv2.imread(img_arr[0] ,   cv2.IMREAD_GRAYSCALE)
    pub.publish(br.cv2_to_imgmsg(n , "8UC1"))

    if time.time() >= init + 2:
        itr += 1 
        init = time.time()
        if itr == len(img_arr):
            itr = 0
            
    # img = cv2.imread("/home/inspire_01/catkin_ws/src/us_volume/test.jpg" , cv2.IMREAD_GRAYSCALE)

    
    rospy.rostime.wallsleep(0.01)

    
