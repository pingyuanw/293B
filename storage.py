import numpy as np 
import anonymize
import datetime
import os
import glob
import cv2
from shutil import copyfile
import toS3

filepath = './data/'
anonymize_path = './anonymized/'
temp_path = './temp/'

def copy_file(label, hash_value):
	if os.path.exists(temp_path+hash_value+".jpg"):
		filename = datetime.datetime.now().strftime("%m-%d-%Y,%H:%M:%S")
		copyfile(temp_path+hash_value+".jpg", filepath+label+"."+filename+".jpg")

def temp_store(filename, data):
	#filename = datetime.datetime.now().strftime("%m-%d-%Y,%H:%M:%S")
	#f = open(filepath+label+'.'+filename+".png",'wb')
	#f.write(data)
	#f.close()
	data.save(temp_path+filename+".jpg","JPEG")


def remove_file(filename):
	if os.path.exists(temp_path+filename+".jpg"):
		os.remove(temp_path+filename+".jpg")


# clear all the png file in foldername
def clear_folder(foldername):
	for subdir, dirs, files in os.walk(foldername):
	for file in files:
		#print os.path.join(subdir, file)
		filepath = subdir + os.sep + file

		if filepath.endswith(".png"):
			print (filepath)
			if os.path.exists(filepath):
				os.remove(filepath)
	print("clear compeleted")

def sent_storage(dest):
	#todo anonymize img before sending.
	files = glob.glob(filepath+'*')
	for f in files:
		print(f)
		new_img = anonymize.anonymize(str(f))
		cv2.imwrite(anonymize_path+str(f)[7:], new_img)
	

	# send the file
	# if we one to send compress then send the zip file, pass in True
	# if we want to send file one by one pass in false, be very careful with passing false,
	# plz look at toS3.py for more detail
	toS3.upload(True)

	#delete contents after send
	#clear_storage(filename)
	clear_folder("anonymized")

if __name__ == '__main__':
	sent_storage(1)

