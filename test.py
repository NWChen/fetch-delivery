import selectormodule as sm
import cv2
import numpy as np 
from time import sleep
#from picamera import PiCamera
#from picamera.array import PiRGBArray
# Create the in-memory stream
#from gopigo import *
#from WheelEncode import *

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


def colorDetect():

	#camera = PiCamera()
	#rawCapture = PiRGBArray(camera)
	camera = cv2.VideoCapture(0)
	sleep(.5)
	shifter_color = np.uint8([10, 40, 40])
	masker = sm.ColorSelector(shifter_color)
	initialArea = None
	initialCentroid = None

	#for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
	while True:

		image = cv2.imread('fetch.jpg')
		masker.loadImage(image)
		mask1 = masker.getMask()

		_,cnts,_ = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(cnts) > 0: 	
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
			# do robotic adjustment based on area ratio or difference
			
			if cx < initialCentroid - 50: #moving out of center:
				print "RIGHT"
			if cx > initialCentroid + 50:
				print "LEFT"

			if abs(cx-initialCentroid) < 50:
				if areaRatio >1.5:
					print "BACKWARD"
					sleep(.1)

				if areaRatio < .7:
					print "FORWARD"
					sleep(.1)


		if cv2.waitKey(10)==27:
			break


