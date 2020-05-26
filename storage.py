import numpy as np 
import anonymize
import datetime
import os
import glob

filepath = './data/'
anonymize_path = './anonymized/'

def store(label, data):
	filename = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	f = open(filepath+label+'-'+filename+".png",'wb+')
	f.write(data)
	f.close()

def clear_storage():
	files = glob.glob(filepath+'*')
	for f in files:
		os.remove(f)


def sent_storage(dest):
	#todo anonymize img before sending.
	files = glob.glob(filepath+'*')
	for f in files:
		new_img = anonymize(f)
		new_f= open(anonymize_path+str(f),'wb')
		new_f.write(data)
		new_f.close()

	# todo sent anonymized img data to s3?

	#delete contents after send
	clear_storage(filename)

	pass

