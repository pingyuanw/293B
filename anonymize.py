import cv2
import numpy as np
import random
from scipy import ndimage

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

def soble_filter(image):
    im = image.astype('int32')
    dx = ndimage.sobel(im, 0) 
    dy = ndimage.sobel(im, 1)
    #calculate hypotenuse
    noisy_image = np.hypot(dx, dy)
    noisy_image *= 255.0 / np.max(noisy_image)
    return noisy_image

def anonymize(imgname):

    image = cv2.imread(imgname)
    if(random.random()<0.5):
        noisy_image = salt_and_pepper(image,0.05)
    else:
        noisy_image = soble_filter(image)

    return noisy_image