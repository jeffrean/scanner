import numpy as np
from math import radians, cos, sin

#units cm, radians
LASER_ANGLE = radians(30.0)
ORIGIN_DEPTH = 14.0
FOCAL_LENGTH = (640.0 * 129.54) / 172.72
FOV = radians(70.0)

class PointCloud:
	def __init__(self, shape):
		self.points = np.zeros(shape)
		self.point_index = 0

	def add_points(self, points):
		self.points[self.point_index] = points
		self.point_index += 1

	def write_to_csv(self):
		with open('points.csv', 'w') as csvfile:
			for i in range(self.point_index):
				for j in range(len(self.points[i])):
					if not np.array_equal(self.points[i][j], np.array([0.0,0.0,0.0])):
						csvfile.write('{point[0]},{point[1]},{point[2]}\n'.format(point=self.points[i][j]))

	def write_to_obj(self):
		objfile = open('points.OBJ', 'w')

		#maintain obj vertex number for polygon connections
		count = 1
		objmap = np.zeros(self.points.shape[0:2], dtype=int)
		for i in range(self.point_index):
			for j in range(len(self.points[i])):
				if not np.array_equal(self.points[i][j], np.array([0.0,0.0,0.0])):
					objfile.write('v {point[0]} {point[1]} {point[2]}\n'.format(point=self.points[i][j]))
					objmap[i][j] = count
					count += 1

		for i in range(self.point_index):
			#find lower (index) bounds for nonzero values
			left_lower_bound = 0
			for j in range(len(self.points[i])):
				if objmap[i][j]:
					left_lower_bound = j
					break

			right_lower_bound = 0
			for j in range(len(self.points[(i + 1) % self.point_index])):
				if objmap[(i + 1) % self.point_index][j]:
					right_lower_bound = j
					break


			#larger line -> smaller numerical value, same for bound
			larger_index = i if left_lower_bound <= right_lower_bound else (i + 1) % self.point_index
			smaller_index = i if left_lower_bound > right_lower_bound else (i + 1) % self.point_index
			larger_bound = left_lower_bound if left_lower_bound <= right_lower_bound else right_lower_bound
			smaller_bound = left_lower_bound if left_lower_bound > right_lower_bound else right_lower_bound

			print(larger_bound)
			print(smaller_bound)

			for j in range(0, len(self.points[smaller_index]) - 1 - smaller_bound, 2):
				objfile.write('f {objmap[smaller_index][smaller_bound + j]} {objmap[larger_index][larger_bound + j]} \
{objmap[smaller_index][smaller_bound + j + 1]} {objmap[larger_index][larger_bound + j + 1]}\n'.format(objmap=objmap, 
					smaller_index=smaller_index, smaller_bound=smaller_bound, larger_index=larger_index, larger_bound=larger_bound, j=j))

			if len(self.points[larger_index]) - (larger_bound + len(self.points[smaller_index]) - 1 - smaller_bound) >= 3:
				final_polygon = 'f {objmap[smaller_index][len(self.points[smaller_index]) - 1]}'.format(objmap=objmap, 
					smaller_index=smaller_index, smaller_bound=smaller_bound, larger_index=larger_index, larger_bound=larger_bound)
				for j in range(larger_bound + len(self.points[smaller_index]) - 1 - smaller_bound, len(self.points[larger_index])):
					final_polygon += ' {objmap[larger_index][j]}'.format(objmap=objmap, larger_index=larger_index)

				objfile.write(final_polygon + '\n')

		objfile.close()

def actual_depths(laser_centers):
	return np.full(laser_centers.shape, ORIGIN_DEPTH)

def calculate_points(laser_centers, frame_width, rotation_angle):
	'''
	TODO: implement angle of platform shifting
	'''
	depths = actual_depths(laser_centers)
	x = ((laser_centers - frame_width) * depths) / FOCAL_LENGTH
	y = x / np.tan(LASER_ANGLE)

	rotation_mat = np.array([[cos(-rotation_angle), -sin(-rotation_angle)],
		[sin(-rotation_angle), cos(-rotation_angle)]])

	xy = np.matmul(np.column_stack((x, y)), rotation_mat)

	z = np.zeros(laser_centers.shape)
	start_index = 0
	max_height = len(laser_centers)
	results = np.argwhere(laser_centers != 0)
	if len(results):
		start_index = results[0][0]
		#z = np.zeros(len(laser_centers) - start_index)
		
		for i in range(start_index, len(laser_centers)-1):
			#flip height as small index -> big height
			z[i] = (max_height - i) * depths[i] / FOCAL_LENGTH
	else:
		raise Exception('No laser points detected')

	#points = np.column_stack((x[start_index:], y[start_index:], z))
	points = np.column_stack((xy, z))
	return points

