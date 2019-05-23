import numpy as np

class PointCloud:
	def __init__(self, size):
		self.points = np.empty((size, 3))
		self.index = 0

	def add_point(point):
		self.points[self.index] = point
		self.index += 1

	def write_to_csv(self):
		with open('points.csv', 'w') as csvfile:
			for i in range(self.index):
				csvfile.write('{point[0]},{point[1]},{point[2]}\n'.format(point=self.points[i]))