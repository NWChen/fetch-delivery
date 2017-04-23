import csv
import copy
import actionlib
import rospy
import roslib

from moveit_python import (MoveGroupInterface,
                            PlanningSceneInterface,
                            PickPlaceInterface)
from moveit_python.geometry import rotate_pose_msg_by_euler_angles

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from moveit_msgs.msg import PlaceLocation, MoveItErrorCodes

def follow():
    pub = rospy.Publisher("/base_controller/command", Twist, queue_size=10)
    rospy.init_node("follow", anonymous=True)
    rate = rospy.Rate(15)

def 

    while not rospy.is_shutdown():
        msg.linear.x = 0 # Temporary; forces the robot to turn only
        msg.angular.z = 
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__";
    try:
        follow()
    except rospy.ROSInterruptException:
        pass


    move_base = MoveBaseClient()
    while not rospy.is_shutdown():
        
