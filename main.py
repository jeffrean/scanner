import cv2

NUM_STEPS = 360

video = cv2.VideoCapture(0)

for step in range(0,NUM_STEPS):
	ret, frame = video.read()
	cv2.imshow('Video', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows()