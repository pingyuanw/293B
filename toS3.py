import boto3


# filename need to include the path
# Key = dest file in the cloud,  body = src file in the edge
def upload(filename,destfile):
	s3 = boto3.resource('s3')

	s3.Bucket('hummingbird-293').put_object(Key = filename, Body=destfile)


# example function called for upload
# upload('edgeTeam/dog-05-26-2020.png','anonymized/dog-05-26-2020,12/21/14.png')