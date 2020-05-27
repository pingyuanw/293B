import numpy as np 
import anonymize
import datetime
import os
import glob
import cv2

filepath = './data/'
anonymize_path = './anonymized/'

def store(label, data):
	filename = datetime.datetime.now().strftime("%m-%d-%Y,%H:%M:%S")
	#f = open(filepath+label+'.'+filename+".png",'wb')
	#f.write(data)
	#f.close()
	data.save(filepath+label+'.'+filename+".jpg","JPEG")


def clear_storage():
	files = glob.glob(filepath+'*')
	for f in files:
		os.remove(f)


def sent_storage(dest):
	#todo anonymize img before sending.
	files = glob.glob(filepath+'*')
	for f in files:
		print(f)
		new_img = anonymize.anonymize(str(f))
		cv2.imwrite(anonymize_path+str(f)[7:], new_img)
	

	# todo sent anonymized img data to s3?

	#delete contents after send
	#clear_storage(filename)

if __name__ == '__main__':
	sent_storage(1)

