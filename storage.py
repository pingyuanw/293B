import numpy as np 
import anonymize
import datetime
import os
import glob
import cv2
from shutil import copyfile
import toS3
import threading


BATCH_SIZE = 2

filepath = './data/'
anonymize_path = './anonymized/'
temp_path = './temp/'
data_folder_count = 0

def copy_file(label, hash_value):
	global data_folder_count
	if os.path.exists(temp_path+hash_value+".jpg"):
		filename = datetime.datetime.now().strftime("%m-%d-%Y,%H-%M-%S")
		copyfile(temp_path+hash_value+".jpg", filepath+label+"/"+label+"-"+filename+".jpg")
		data_folder_count+=1
		if data_folder_count == BATCH_SIZE:
			upload_thread = threading.Thread(target=anonymize_and_upload)
			upload_thread.start()			
			data_folder_count=0

def temp_store(filename, data):
	#filename = datetime.datetime.now().strftime("%m-%d-%Y,%H:%M:%S")
	#f = open(filepath+label+'.'+filename+".png",'wb')
	#f.write(data)
	#f.close()
	data.save(temp_path+filename+".jpg","JPEG")

def anonymize_and_upload():
	print("Starting to send data to cloud...")
	datafolder_to_anonymizedfolder()
	toS3.upload(True)
	clear_folder("anonymized")
	print("Completed sending data to cloud")


def remove_file(filename):
	if os.path.exists(temp_path+filename+".jpg"):
		os.remove(temp_path+filename+".jpg")


# clear all the png file in foldername
def clear_folder(foldername):
	for subdir, dirs, files in os.walk(foldername):
		for file in files:
			#print os.path.join(subdir, file)
			filepath = subdir + os.sep + file

			if filepath.endswith(".jpg"):
				print (filepath)
				if os.path.exists(filepath):
					os.remove(filepath)
	print("clear compeleted")

def datafolder_to_anonymizedfolder():
	count = 0
	for root,dirs,_ in os.walk(filepath):
		for d in dirs:
			files=glob.glob(filepath+str(d)+'/*')
			for f in files:
				# 7 here is the lenegth of ./data/
				new_img = anonymize.anonymize(str(f))
				cv2.imwrite(anonymize_path+str(f)[7:], new_img)
				os.remove(str(f))
				count+=1
				if (count == BATCH_SIZE):
					return

def sent_storage():
	#todo anonymize img before sending.
	datafolder_to_anonymizedfolder()
	

	# send the file
	# if we one to send compress then send the zip file, pass in True
	# if we want to send file one by one pass in false, be very careful with passing false,
	# plz look at toS3.py for more detail
	toS3.upload(True)

	#delete contents after send
	#clear_storage(filename)
	clear_folder("anonymized")
	clear_folder("data")

if __name__ == '__main__':
	datafolder_to_anonymizedfolder()

