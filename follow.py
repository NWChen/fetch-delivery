import csv
import copy
import actionlib
import rospy
import roslib

import selectormodule as sm
import cv2
import numpy as np

from time import sleep
from moveit_python import (MoveGroupInterface,
                            PlanningSceneInterface,
                            PickPlaceInterface)
from moveit_python.geometry import rotate_pose_msg_by_euler_angles

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from moveit_msgs.msg import PlaceLocation, MoveItErrorCodes

RAW_IMAGE = "fetch.jpeg"
shifter_color = np.uint8([10, 40, 40])
masker = sm.ColorSelector(shifter_color)
initialArea, initialCentroid = None, None

def get_direction():
    print "CALLED GET DIRECTION"
    image = cv2.imread(RAW_IMAGE)
    masker.loadImage(image)
    mask = masker.getMask()
    print mask
    direction = ''
    _, cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        print "CNTS LENGTH: " + str(len(cnts))
        blob = findLargestContour(cnts)
        currentArea = cv2.contourArea(blob)
        M = cv2.moments(blob)
        cx = int(M['m10']/M['m00'])

        if initialArea is None:
            initialArea = currentArea
            initialCentroid = cx

        areaRatio = currentArea/initialArea
        print "New Area/Initial Area: ", areaRatio
        print "New Centroid, Initial Centroid", initialCentroid, cx

        if cx < intialCentroid - 50:
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
    pub = rospy.Publisher("/base_controller/command", Twist, queue_size=10)
    rospy.init_node("follow", anonymous=True)
    rate = rospy.Rate(1)

    msg = Twist()
    while not rospy.is_shutdown():
        print "FETCH ALIVE"
        msg.linear.x = 0.0 # Temporary; forces the robot to turn only
        direction = get_direction()
        print direction
        if direction == 'l':
            msg.angular.z = -0.5
        elif direction == 'r':
            msg.angular.z = 0.5
        else:
            msg.angular.z = 0.0
        pub.publish(msg)
        rospy.sleep(rospy.Duration(1,0))

if __name__ == "__main__":
    try:
        follow()
    except rospy.ROSInterruptException:
        pass
