import numpy as np 
import anonymize
import datetime
import os
import glob

filepath = './data/'
anonymize_path = './anonymized/'

def store(label, data):
	filename = datetime.datetime.now().strftime("%m-%d-%Y,%H:%M:%S")
	f = open(filepath+label+'-'+filename+".png",'wb+')
	for byte in data:
		f.write(byte)
	f.close()

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
		new_f= open(anonymize_path+str(f)[7:],'wb+')
		new_f.write(new_img)
		new_f.close()

	# todo sent anonymized img data to s3?

	#delete contents after send
	#clear_storage(filename)

if __name__ == '__main__':
	sent_storage(1)

