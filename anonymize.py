import cv2
import numpy as np
import random

#anonymize dataset before storage

def salt_and_pepper(image,prob):

    output = np.zeros(image.shape,np.uint8)
    delta = 1 - prob 

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            seed = random.random()
            if(seed <= prob):
                output[i][j] = 0
            elif(seed >= delta):
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def anonymize(imgname):
	image = cv2.imread(imgname)


	#noisy_image = image + np.random.normal(mean, sigma, image.shape)

	noisy_image = salt_and_pepper(image,0.05)

	return noisy_image