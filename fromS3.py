import boto3

# buck_name is the name of the buckets
# filename, is the file in S3, with the path
# dest_name is the file name we want to save it as
def downloadFromS3(buc_name,filename,dest_name):
	s3 = boto3.client('s3')
	s3.download_file(buc_name,filename,dest_name)

def checkForUpdate():
	
