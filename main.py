import cv2
import scanner
import vectorspace
import numpy as np

NUM_STEPS = 360

video = cv2.VideoCapture(0)

#create point cloud
ret, frame = video.read()
#pointcloud = vectorspace.PointCloud((NUM_STEPS, frame.shape[0]))
pointcloud = vectorspace.PointCloud((NUM_STEPS, 800, 3))

#for step in range(0,NUM_STEPS):
while True:
	ret, frame = video.read()
	#cv2.imshow('Frame', frame)
	#cv2.imshow('Threshold', thresh)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	if cv2.waitKey(1) & 0xFF == ord('s'):
		thresh = scanner.laser_threshold_image(frame)
		print('calculating laser centers')
		laser_centers = scanner.laser_centers_of_mass(thresh)
		print('calculating points')
		points = vectorspace.calculate_points(laser_centers)
		print('adding points')
		pointcloud.add_points(points)
		'''offset_points = np.copy(points)
		for point in offset_points:
			point[0] += 10
			point[1] -= 10
		pointcloud.add_points(offset_points)'''

pointcloud.write_to_csv()
pointcloud.write_to_obj()
video.release()
cv2.destroyAllWindows()