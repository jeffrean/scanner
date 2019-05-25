import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import pi, cos, sin
import numpy as np

def read_in_vertices():
	vertices = []
	with open('points.csv', 'r') as points_file:
		for line in points_file:
			vertices.append(tuple([float(c) for c in line.split(',')]))
	return vertices

def show(vertices):
	glBegin(GL_POINTS)
	for vertex in vertices:
		glVertex3fv(vertex)
	glEnd()

def main():
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

	vertices = read_in_vertices()

	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

	glTranslatef(0.0,-10.0,-50)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		show(vertices)
		pygame.display.flip()
		pygame.time.wait(10)


main()