import cv2
import scanner
import vectorspace
import numpy as np
from math import radians

NUM_STEPS = 90

video = cv2.VideoCapture(0)

#create point cloud
ret, frame = video.read()
pointcloud = vectorspace.PointCloud((NUM_STEPS, frame.shape[0], 3))

#for step in range(0,NUM_STEPS):
step = 0
while True:
	ret, frame = video.read()
	cv2.imshow('Frame', frame)
	thresh = scanner.laser_threshold_image(frame)
	cv2.imshow('Threshold', thresh)

	#if cv2.waitKey(1) & 0xFF == ord('q'):
		#break
	if cv2.waitKey(1) & 0xFF == ord('s'):
		for step in range(NUM_STEPS):
			print(step)
			thresh = scanner.laser_threshold_image(frame)
			print('calculating laser centers')
			laser_centers = scanner.laser_centers_of_mass(thresh)
			print('calculating points')
			points = vectorspace.calculate_points(laser_centers, frame.shape[1], radians(step * 4))
			print('adding points')
			pointcloud.add_points(points)
			print('done')
			step += 1
		break

pointcloud.write_to_csv()
pointcloud.write_to_obj()
video.release()
cv2.destroyAllWindows()