import csv
# import rospy
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def choose_location(locations):
	print("--------------------")
	index = 0
	for loc in locations:
		print(index, loc[0])
		index += 1

	print("--------------------")

	print("Enter the index of the location")
	loc_index = input()
	return locations[int(loc_index)]

def main():
	input_file = "navigation_labels.txt"
	coordinates = []
	with open(input_file, 'r') as f:
		reader = csv.reader(f)
		coordinates = list(reader)

	# locations = [row[0] for row in coordinates]

	point = choose_location(coordinates)

	print(point)

	# goal = MoveBaseGoal()
	# goal.target_pose.pose.position = Point()



main()