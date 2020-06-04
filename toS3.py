import boto3
import zipfile
import os
import datetime

# This function is used to compress directory in zip file
def zipdir(path, ziph):
	# ziph is zipfile handle
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))

# filename need to include the path
# Key = dest file in the cloud,  body = src file in the edge
def upload(compressOrNot):
	s3 = boto3.resource('s3')
	# There are two ways to send the file to S3
	# if you set it to true, then we send it one img at a time
	# if you set compressOrNot to TRUE, then we compress the file and send it

	# compressOrNot = True

	# WARNING if we choosee compressOrNot to False, it means send every pg file in anonymized folder
	# we need to make sure that there are not many files so we don't waste the spend
	if compressOrNot == False:
		# sent anonymized img data to s3
		for subdir, dirs, files in os.walk("anonymized"):
			for file in files:
				#print os.path.join(subdir, file)
				filepath = subdir + os.sep + file

				if filepath.endswith(".png"):
					print (filepath)
					# uncomment line below if u are sure u one to send file one by one
					# s3.Bucket('hummingbird-293').put_object(Key = 'edgeTeam/'+filepath, Body=filepath)
					print("send completed")
	else:
		filename = 'anonymized-'+str(datetime.datetime.now().strftime("%m-%d-%Y,%H-%M-%S"))+'.zip'
		zipf = zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED)
		zipdir('anonymized',zipf)
		zipf.close()
		# key is the dest file, body is the src file
		s3.Bucket('hummingbird-293').upload_file(Key = 'edgeTeam/'+filename, Filename='/home/ishtiyaque/293B/'+filename)
		os.remove(filename)
		print("send completed")



# example function called for upload
# upload(True)