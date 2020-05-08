import numpy as np 
filename = "data.txt"

def store(data):
	f = open(filename, "w")
	f.write(data)
	f.write('\n')
	f.close()

def clear_storage():
	open(filename, 'w').close()

def sent_storage(dest):
	# todo sent all stored data to s3?

	clear_storage(filename)

