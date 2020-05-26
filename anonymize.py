import cv2
import numpy

#anonymize dataset before storage
def anonymize(imgname, factor = 0.2):
	img = cv2.imread(imgname)
	(h, w) = img.shape[:2]
	
	delta_W = int(w / factor)
	delta_H = int(h / factor)

	if delta_W % 2 == 0:
		delta_W -= 1
	if delta_H % 2 == 0:
		delta_H -= 1

	result = cv2.GaussianBlur(img, (delta_W, delta_H), 0)

	cv2.imshow('result', result)

	return result