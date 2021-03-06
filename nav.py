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

# from sqlalchemy import *
# from sqlalchemy.pool import NullPool
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
#app.debug=True
x = 0
y = 0

NAV_FILE = "/home/nwchen/fetch_ws/src/fetch_gazebo/fetch_gazebo_demo/scripts/navigation_labels.txt"

@app.route('/')
def index():
    nav_list = []
    with open(NAV_FILE, 'r') as f:
        reader = csv.reader(f)
        nav_list = list(reader)
        f.close()

    print nav_list

    data = []
    for loc in nav_list:
        entry_dict = {"location": loc[0], "x": loc[1], "y": loc[2]}
        data.append(entry_dict)

    context = dict(data = data)
    return render_template('index.html', **context)

@app.route('/pos', methods=['GET', 'POST'])
def pos():
    location_name = ''
    if request.get_json() != None:
        location_name = request.get_json()['location']
    global x
    global y
    if location_name != '':
        print(location_name)
        nav_list = []
        with open(NAV_FILE, 'r') as f:
            reader = csv.reader(f)
            nav_list = list(reader)
            f.close()

        x_pos = 0
        y_pos = 0
        for loc in nav_list:
            if loc[0] == location_name:
                x_pos = float(loc[1])
                y_pos = float(loc[2])
                x = x_pos
                y = y_pos
                # print"GOING TO " + location_name
                # print x, y

        x = x_pos
        y = y_pos
        # print "X: " + str(x)
        # print "Y: " + str(y)
        print("x_speech", x)
        print("y_speech", y)
        return render_template('index.html')
    else:
        loc_form_x = ''
        loc_form_y = ''
        x_pos = 0
        y_pos = 0
        if request.method == 'POST':
            loc_form_x = request.form['x']
            loc_form_y = request.form['y']
            x_pos = float(loc_form_x)
            y_pos = float(loc_form_y)

        x = x_pos
        y = y_pos
        print("x_form", x)
        print("y_form", y)
        return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    error = ""

    if request.method == 'POST':
        name = request.form['name']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']

        out_file = open("navigation_labels.txt", 'a')
        out_file.write('\n' + name + ", " + x + ", " + y)
        out_file.close()

        # try:
        #   g.conn.execute('INSERT INTO locations(name, x, y, z) VALUES ((%s), (%s), (%s), (%s))', name, x, y, z)
        # except:
        #   error = "error inserting location"

    return render_template('add.html', error=error)

def start_server():
    app.run(host=host, port=port, threaded=True)

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
    #rospy.loginfo(rospy.get_param("/use_sim_time"))

    host = "0.0.0.0"
    port = 5000

    #start_server()

    # start webserver on a separate thread from ros
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    #rospy.loginfo(rospy.get_param("/use_sim_time"))
    # # Make sure sim time is working
    while not rospy.Time.now():
        pass

    # # Setup clients
    move_base = MoveBaseClient()

    print ("SERVER AND CLIENT STARTED UP")
    rate = rospy.Rate(15)

    testCalled = False

    while not rospy.is_shutdown():

        # rospy.loginfo(rospy.get_param("/use_sim_time"))

        # prevent assumption that destination is (0, 0)
        if x == 0.3:
            testCalled = True
        if x == 0 and y == 0:
            continue
        rospy.loginfo(x)
        rospy.loginfo(y)
        print "MOVING BASE TO " + str(x) + ", " + str(y)
        #if testCalled != True:
        move_base.goto(x, y, 0.0)
        rate.sleep()
