# import the necessary packages
import numpy as np
import argparse
import cv2
from operator import add


class ColorSelector:
	"""A class that serves as an eyedropper mask tool. Allows user to 
	select a color range and then creates a mask based on that"""

	def __init__(self, shift_color= np.uint8([30,100,100])):
		self.image = None
		self.lwr = None
		self.upr = None
		self.clickPoints = []

		self.setWindow()
		self.shifter = shift_color


	def loadImage(self,image):
		self.image = image


	# Creates an eyedropper tool and allows you to select the high and low 
	# values for the color range
	def getColor(self,event, x, y, flags, param):		
		if event == cv2.EVENT_LBUTTONDOWN:
			self.clickPoints= self.clickPoints + [(y,x)]
			print self.clickPoints
			if len(self.clickPoints) == 2:
				self.lwr, self.upr = self.getColorRange()
				self.clickPoints = []

	def setWindow(self):
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", self.getColor)
			

	# Creates a mask out of the image and the color range
	def getMask(self):
		h,w=self.image.shape[:2]
		print "HEIGHT %d", h
		print "WIDTH %d", w
        self.image = cv2.resize(self.image,((int(w*.5),int(h*.5))), interpolation = cv2.INTER_AREA)
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", self.getColor)
		cv2.imshow("image",self.image)

		mask = np.zeros( (int(h*.5),int(w*.5),), dtype = "uint8")

		if self.lwr is not None and self.upr is not None:
			
			#creates the mask using the inRange function
			hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(hsv,self.lwr, self.upr)

			#performs some dilations and erosions to regularize mask
			mask = cv2.medianBlur(mask,11)
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
			kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
			mask = cv2.erode(mask, kernel, iterations = 4)
			mask = cv2.dilate(mask, kernel2, iterations = 4)

		cv2.imshow('mask',mask)
		return mask

	def getColorRange(self):
		minY = min(self.clickPoints ,key= lambda t: t[0])[0]
		maxY = max(self.clickPoints ,key= lambda t: t[0])[0]

		minX = min(self.clickPoints ,key= lambda t: t[1])[1]
		maxX = max(self.clickPoints ,key= lambda t: t[1])[1]

		window = self.image[minY:maxY,minX:maxX]
		window = cv2.cvtColor(window,cv2.COLOR_BGR2HSV)
		avgColorRows = np.average(window,axis=0)
		avgColor = np.uint8(np.average(avgColorRows,axis=0))

		lowColor = cv2.subtract(avgColor,self.shifter)
		highColor = cv2.add(avgColor,self.shifter)

		# color = np.zeros((300,300,3), dtype = "uint8")
		# color[:,:,:] = avgColor
		# cv2.imshow('color', color)

		print "tracking color", avgColor 

		return (lowColor,highColor)


