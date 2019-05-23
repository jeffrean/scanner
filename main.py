import cv2
import scanner

NUM_STEPS = 360

video = cv2.VideoCapture(0)

#for step in range(0,NUM_STEPS):
while True:
	ret, frame = video.read()
	thresh = laser_threshold_image(frame)
	cv2.imshow('Video', thresh)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows()