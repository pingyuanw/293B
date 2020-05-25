import numpy as np 
import anonymize
import datetime
import os
import glob

filepath = './data/'

def store(label, data):
	filename = datetime.datetime.now()
	f = open(filepath+label+'.'filename+".png",'wb')
	f.write(data)
	f.close()

def clear_storage():
	files = glob.glob(filepath+'*')
	for f in files:
		os.remove(f)


def sent_storage(dest):
	#todo anonymize img before sending.
	anonymized_img_list = []
	for f in files:
		anonymized_img_list.append(anonymize(f))

	# todo sent anonumized img data to s3?

	#delete contents after send
	clear_storage(filename)

	pass

