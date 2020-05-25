import boto3
import datetime
# buck_name is the name of the buckets in ''
# filename, is the file in S3, with the path in ''
# dest_name is the file name we want to save it as in ''
def downloadFromS3(buc_name,filename,dest_name):
	s3 = boto3.client('s3')
	s3.download_file(buc_name,filename,dest_name)

# buc_name is the name of the buckets in ''
# this returns the last modified date of the model
# we want to use this output in compareDate to see if that is the most 
# recently used file
def getLastModified(buc_name):
	s3 = boto3.client('s3')
	listOfFiles = s3.list_objects_v2(Bucket='hummingbird-293')['Contents']
	# need a proper search alg, implemented later on
	modelfile = listOfFiles[1]
	lastModified = modelfile['LastModified']

	return lastModified

# this takes the original date and current date, compare them
# if they are not equal that means, we need a update of model
# return true means we need an update
def compareDate(original_date, current_date):
	return not(original_date==current_date)

# an helper method that is used to find the file of model
def findModelfiles(listOfFiles):


# print(getLastModified('hummingbird-293'))


