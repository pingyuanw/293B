import numpy as np 

def storage(data, filename):
	f = open(filename, "w")
	f.write(data)
	f.write('\n')
	f.close()

def clear_storage(filename):
	open(filename, 'w').close()

def sent_storage(filename, dest):
	# todo sent all stored data to s3?

	clear_storage(filename)

