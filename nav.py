#!/usr/bin/python

import csv
import copy
import actionlib
import rospy
import roslib

import threading

from math import sin, cos
from moveit_python import (MoveGroupInterface,
                           PlanningSceneInterface,
                           PickPlaceInterface)
from moveit_python.geometry import rotate_pose_msg_by_euler_angles

from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from moveit_msgs.msg import PlaceLocation, MoveItErrorCodes

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
x = 0
y = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pos', methods=['GET', 'POST'])
def pos():
    location_name = request.args.get('location')
    nav_list = []
    with open("navigation_labels.txt", 'r') as f:
        reader = csv.reader(f)
        nav_list = list(reader)
        f.close()

    global x
    global y
    for loc in nav_list:
        if loc[0] == location_name:
            x = float(loc[1])
            y = float(loc[2])

    # x = float(request.form['x'])
    # y = float(request.form['y'])
    print "X: %d, Y: %d" % (x, y)
    return render_template('index.html')



def start_server():
    app.run(host=host, port=port)

# Move base using navigation stack
class MoveBaseClient(object):

    def __init__(self):
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.client.wait_for_server()

    def goto(self, x, y, theta, frame="map"):
        move_goal = MoveBaseGoal()
        move_goal.target_pose.pose.position.x = x
        move_goal.target_pose.pose.position.y = y
        move_goal.target_pose.pose.orientation.z = sin(theta/2.0)
        move_goal.target_pose.pose.orientation.w = cos(theta/2.0)
        move_goal.target_pose.header.frame_id = frame
        move_goal.target_pose.header.stamp = rospy.Time.now()

        # TODO wait for things to work
        self.client.send_goal(move_goal)
        self.client.wait_for_result()

if __name__ == "__main__":
    # Create a node
    rospy.init_node("demo")

    host = "0.0.0.0"
    port = 5000

    # start webserver on a separate thread from ros
    t = threading.Thread(target=start_server)
    t.daemon=True
    t.start()

    # Make sure sim time is working
    while not rospy.Time.now():
        pass

    # Setup clients
    move_base = MoveBaseClient()

    while not rospy.is_shutdown():

        # prevent assumption that destination is (0, 0)
        if x == 0 and y == 0:
            continue
        rospy.loginfo(x)
        rospy.loginfo(y)
        move_base.goto(x, y, 0.0)
