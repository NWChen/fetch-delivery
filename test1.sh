#!/bin/bash

source ~/fetch_ws/devel/setup.bash 
roslaunch fetch_gazebo playground.launch & 
sleep 10s
source ~/fetch_ws/devel/setup.bash 
roslaunch fetch_navigation fetch_nav.launch map_file:=$1 & 
sleep 10s
#source ~/fetch_ws/devel/setup.bash
#roslaunch fetch_navigation build_map.launch &
#sleep 10s
source ~/fetch_ws/devel/setup.bash 
rosrun rviz rviz &
#sleep 30s
#echo "saving map to file"
#source ~/fetch_ws/devel/setup.bash
#rosrun map_server map_saver -f ~/testmap.yaml
echo "done"
