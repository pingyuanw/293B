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
# if coulndt locate model, return a date in 2000, and print Does not find
def getLastModified():
	s3 = boto3.client('s3')
	listOfFiles = s3.list_objects_v2(Bucket='hummingbird-293')['Contents']
	# need a proper search alg, implemented later on
	index = findModelfiles(listOfFiles)
	if index > -1:
		modelfile = listOfFiles[index]
		lastModified = modelfile['LastModified']
	else:
		print("Does not find model")
		return datetime.datetime(2000,1,1,0,0,0,0,tzinfo=datetime.timezone.utc)

	return int(lastModified.timestamp())

# this takes the original date and current date, compare them
# if they are not equal that means, we need a update of model
# return true means we need an update
def compareDate(original_date, current_date):
	# check if the crrent_date is a valid date
	if current_date == datetime.datetime(2000,1,1,0,0,0,0,tzinfo=datetime.timezone.utc):
		print("File not found")
		return False
	return (original_date<current_date)

# A helper method that is used to find the file of model
# returns the index of corresponding file
# if index = -1 that means not found
def findModelfiles(listOfFiles):
	index = 0
	for e in listOfFiles:
		if e['Key']=='Models/resnet50_ckpt.pth':
			return index
		index = index + 1
	index = -1
	return index


# below were used to test the function
# print(getLastModified('hummingbird-293'))
# test = datetime.datetime(2020,5,15,7,38,25,0,tzinfo=datetime.timezone.utc)
# print(test)
# print(compareDate(test,getLastModified('hummingbird-293')))


