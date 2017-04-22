#!/usr/bin/env python2.7
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

### Neil's imports
# import csv
# import copy
# import actionlib
# import rospy
# import roslib

# import threading

# from math import sin, cos
# from moveit_python import (MoveGroupInterface,
#                            PlanningSceneInterface,
#                            PickPlaceInterface)
# from moveit_python.geometry import rotate_pose_msg_by_euler_angles

# from geometry_msgs.msg import PoseStamped
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# from moveit_msgs.msg import PlaceLocation, MoveItErrorCodes

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://myq2000:7644@104.196.135.151/proj1part2"
engine = create_engine(DATABASEURI)

x = 0
y = 0

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
    cursor = g.conn.execute("SELECT L.name, L.x, L.y, L.z FROM locations L")
    data = []
    for result in cursor:
      entry_dict = {"location": result[0], "x": result[1], "y": result[2], "z": result[3]}
      data.append(entry_dict)
    cursor.close()

    context = dict(data = data)

    return render_template('index.html', **context)

@app.route('/add', methods=['GET', 'POST'])
def add():
  error = ""

  if request.method == 'POST':
    name = request.form['name']
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']

    try:
      g.conn.execute('INSERT INTO locations(name, x, y, z) VALUES ((%s), (%s), (%s), (%s))', name, x, y, z)
    except:
      error = "error inserting location"

  return render_template('add.html', error=error)


@app.route('/pos/', methods=['POST'])
def pos():
    global x
    global y
    x = float(request.form['x'])
    y = float(request.form['y'])
    print("X: %d, Y: %d" % (x, y))
    return render_template('index.html')


# # Move base using navigation stack
# class MoveBaseClient(object):

#     def __init__(self):
#         self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
#         rospy.loginfo("Waiting for move_base...")
#         self.client.wait_for_server()

#     def goto(self, x, y, theta, frame="map"):
#         move_goal = MoveBaseGoal()
#         move_goal.target_pose.pose.position.x = x
#         move_goal.target_pose.pose.position.y = y
#         move_goal.target_pose.pose.orientation.z = sin(theta/2.0)
#         move_goal.target_pose.pose.orientation.w = cos(theta/2.0)
#         move_goal.target_pose.header.frame_id = frame
#         move_goal.target_pose.header.stamp = rospy.Time.now()

#         # TODO wait for things to work
#         self.client.send_goal(move_goal)
#         self.client.wait_for_result()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  # # start webserver on a separate thread from ros
  # t = threading.Thread(target=run)
  # t.daemon=True
  # t.start()

  # # Make sure sim time is working
  # while not rospy.Time.now():
  #     pass

  # # Setup clients
  # move_base = MoveBaseClient()

  # while not rospy.is_shutdown():

  #     # prevent assumption that destination is (0, 0)
  #     if x == 0 and y == 0:
  #         continue
  #     rospy.loginfo(x)
  #     rospy.loginfo(y)
  #     move_base.goto(x, y, 0.0)


  run()
