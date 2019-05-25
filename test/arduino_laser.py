import cv2
import numpy as np

def laser_threshold_image(frame):
	'''gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)
	thresh = cv2.threshold(blurred, 210, 255, cv2.THRESH_BINARY)[1]'''
	#blurred = cv2.blur(frame,(5,5))

	#color
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	dark_red = cv2.cvtColor(np.uint8([[[187,47,85]]]),cv2.COLOR_RGB2HSV)[0][0]
	lower_red = np.uint8([[[dark_red[0] - 50, dark_red[1] - 50, dark_red[2] - 50]]])
	upper_red = np.uint8([[[dark_red[0] + 90, dark_red[1] + 90, dark_red[2] + 90]]])
	mask = cv2.inRange(hsv, lower_red, upper_red)

	#brightness
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (9, 9), 0)
	thresh = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)[1]

	#edge
	edge = cv2.Canny(cv2.split(hsv)[0], 50, 100)
	mask_thresh = cv2.bitwise_or(mask, thresh)
	return cv2.bitwise_and(mask_thresh, edge)

def linear_interpolate(laser_centers):
	empty_flag = False
	empty_ranges = []
	for i in range(len(laser_centers) - 1):
		if laser_centers[i] != 0 and laser_centers[i + 1] == 0 and not empty_flag:
			empty_flag = True
			empty_ranges.append(i)
		elif laser_centers[i + 1] != 0 and empty_flag:
			empty_flag = False
			empty_ranges.append(i + 1)

	if empty_flag:
		#del empty_ranges[-1]
		empty_ranges.append(empty_ranges[-1])

	for i in range(0, len(empty_ranges), 2):
		rise = empty_ranges[i+1] - empty_ranges[i]
		run = laser_centers[empty_ranges[i+1]] - laser_centers[empty_ranges[i]]
		slope = rise / run

		x = laser_centers[empty_ranges[i]]
		for j in range(empty_ranges[i] + 1, empty_ranges[i+1]):
			#x2 = (y2 - y1 + mx1) / m
			if np.isinf(slope):
				laser_centers[j] = laser_centers[j-1]
			else:
				x = (j - (j-1) + slope * x) / slope
				laser_centers[j] = int(x)


def laser_centers_of_mass(frame):
	laser_centers = np.zeros(frame.shape[0])
	#keep track of undetected laser spots
	empty_flag = False

	for i in range(frame.shape[0]):
		count = 0
		for j in range(frame.shape[1]):
			if frame[i][j] != 0:
				laser_centers[i] += j
				count += 1

		if count != 0:
			laser_centers[i] //= count
		else:
			empty_flag = True


	if empty_flag:
		linear_interpolate(laser_centers)

	return laser_centers

def laser_center_of_mass_draw(frame):
	laser_centers = laser_centers_of_mass(frame)
	new_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
	for i in range(len(laser_centers)):
		if not np.isnan(laser_centers[i]):
			new_frame[i][int(laser_centers[i])][0] = 255
			#new_frame[i][int(laser_centers[i])][1] = 255
			#new_frame[i][int(laser_centers[i])][2] = 255
	return new_frame

img = cv2.imread('laser.png', 1)
thresh = laser_threshold_image(img)
cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
cv2.namedWindow('Threshold',cv2.WINDOW_NORMAL)
cv2.imshow('Frame', img)
cv2.resizeWindow('Frame', 400, 350)
new = laser_center_of_mass_draw(thresh)
cv2.imshow('Threshold', new)
cv2.resizeWindow('Threshold', 400, 350)

while True:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()