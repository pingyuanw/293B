import numpy as np 
import anonymize
import datetime
import os
import glob

filepath = './data/'

def store(data):
	data = anonymize.anonymize(data)

	filename = datetime.datetime.now()
	f = open(filepath+filename+".png",'wb')
	f.write(data)
	f.close()

def clear_storage():
	files = glob.glob(filepath+'*')
	for f in files:
		os.remove(f)


def sent_storage(dest):
	# todo sent all stored data to s3?

	#delete contents after send
	#clear_storage(filename)

	pass

