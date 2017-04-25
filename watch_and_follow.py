import csv
import copy
import actionlib
import rospy
import roslib
import math

import selectormodule as sm
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
from time import sleep
from moveit_python import (MoveGroupInterface,
                            PlanningSceneInterface,
                            PickPlaceInterface)
from moveit_python.geometry import rotate_pose_msg_by_euler_angles

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from moveit_msgs.msg import PlaceLocation, MoveItErrorCodes

shifter_color = np.uint8([10, 40, 40])
masker = sm.ColorSelector(shifter_color)
initialArea = None
initialCentroid = None
bridge = CvBridge()
raw = None

def callback(data):
    global raw
    try: 
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
        print e
        return None
    else:
        raw = img

def findLargestContour(contours):
    max_area = 0
    maxIndex = -1
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if(area > max_area):
            max_area = area
            maxIndex = i
    return contours[maxIndex]

def get_direction():
    global raw
    direction = ''

    if raw == None:
        return None

    try:
        image = raw
    except AttributeError:
        return None
    else:
        cv2.imshow('FETCH', image)
        masker.loadImage(image)
        mask = masker.getMask()
        print mask
        _, cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            print "CNTS LENGTH: " + str(len(cnts))
            blob = findLargestContour(cnts)
            currentArea = cv2.contourArea(blob)
            M = cv2.moments(blob)
            cx = int(M['m10']/M['m00'])

            global initialArea
            global initialCentroid
            if initialArea == None:
                initialArea = currentArea
                initialCentroid = cx

            areaRatio = currentArea/initialArea
            print "New Area/Initial Area: ", areaRatio
            print "New Centroid, Initial Centroid", initialCentroid, cx

            if cx < initialCentroid - 50:
                print "LEFT"
                direction = 'l'
            if cx > initialCentroid + 50:
                print "RIGHT"
                direction = 'r'

            if abs(cx - initialCentroid) < 50:
                if areaRatio > 1.5:
                    print "BACKWARD"
                    direction = 'b'
                if areaRatio < 0.7:
                    print "FORWARD"
                    direction = 'f'
    return direction

def follow():
    rospy.init_node('follow', anonymous=True)
    #rospy.init_node('watch', anonymous=True)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/head_camera/rgb/image_raw', Image, callback)
    #rospy.spin()

    msg = Twist()
    while not rospy.is_shutdown():
        print "FETCH ALIVE"
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        direction = get_direction()
        print direction
        if direction == 'l':
            msg.angular.z = math.radians(45)
        elif direction == 'r':
            msg.angular.z = math.radians(-45)
        elif direction == 'f':
            msg.linear.x = 0.5
        elif direction == 'b':
            msg.linear.x = -0.5
        print "ANGULAR Z: " + str(msg.angular.z)
        print "LINEAR  X: " + str(msg.linear.x)
        pub.publish(msg)
        rospy.sleep(0.2)

if __name__ == "__main__":
    try:
        follow()
    except rospy.ROSInterruptException:
        pass
