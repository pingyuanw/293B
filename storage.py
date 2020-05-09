import numpy as np 
import anonymize

filename = "data.txt"

def store(data):
	data = anonymize.anonymize(data)
	f = open(filename, "a")
	f.write(data)
	f.write('\n')
	f.close()

def clear_storage():
	open(filename, 'w').close()

def sent_storage(dest):
	# todo sent all stored data to s3?

	clear_storage(filename)

