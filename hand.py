import selectormodule as sm
import cv2
import numpy as np 
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
# Create the in-memory stream
from gopigo import *
from WheelEncode import *

def findLargestContour(contours):
	max_area = 0
	maxIndex = -1
	for i in range(len(contours)):
		cnt=contours[i]
		area = cv2.contourArea(cnt)
		if(area>max_area):
			max_area=area
			maxIndex=i
	return contours[maxIndex]


camera = PiCamera()
rawCapture = PiRGBArray(camera)
sleep(.5)
masker = sm.ColorSelector()
initialArea = None
initialCentroid = None
verticalInitialCentroid = None

for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
	# _ret, image = cap.read()
	image = frame.array
	image = cv2.flip(image,1)
	masker.loadImage(image)
	mask1 = masker.getMask()


	_,cnts,_ = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if len(cnts) > 0: 	
		blob=findLargestContour(cnts)
		currentArea = cv2.contourArea(blob)
		M = cv2.moments(blob)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		if initialArea is None:
			initialArea = currentArea
			initialCentroid = cx
			verticalInitialCentroid = cy

		areaRatio = currentArea/initialArea
		print "New Area/Initial Area: ", areaRatio
		print "New Centroid, Initial Centroid, Vertical Initial Cenroid", initialCentroid, cx, cy
		# do robotic adjustment based on area ratio or difference
		
		if cx < initialCentroid-50: #moving out of center:
			right_deg(10)
		if cx > initialCentroid+50:
			left_deg(10)
		if cy < verticalInitialCentroid-50:
			fwd_cm(6)
		if cy > verticalInitialCentroid+50:
			bwd_cm(6)





		#same thing with centroid (really only x centroid matters because it can only rotate left right not up down)
	rawCapture.truncate(0)
	if cv2.waitKey(10)==27:
		break


