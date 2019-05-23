import numpy as np
import cv2

def laser_threshold_image(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)
	thresh = cv2.threshold(blurred, 210, 255, cv2.THRESH_BINARY)[1]
	return thresh

def calculate_depth()
	pass