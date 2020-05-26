#communicate with client
import socket
import sys
import os
import storage
import inference
from struct import *


TCP_IP = '127.0.0.1'#localhost
TCP_PORT = 5000
BUFFER_SIZE = 1024

aws_access_key_id='Secret'
aws_secret_access_key='Secret'


#inference_handler = inference.Inference(aws_access_key_id, aws_secret_access_key)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
connection, client_address = sock.accept()

while(1):
	data = connection.recv(4)
	filesize = unpack('!I', data)[0]
	print("file size is: "+str(filesize))

	data = []
	msg = connection.recv(BUFFER_SIZE)
	recieved = 1024
	
	while(recieved<filesize):
		recieved+=BUFFER_SIZE
		data += msg
		msg = connection.recv(BUFFER_SIZE)
		print("receiving")
	print("done receiving ...")

	#response = inference_handler.predict(data)
	response = 'dog'

	response_size = pack('!I', len(response))
	connection.send(response_size)

	connection.send(response.encode())

	
	connection.send("do we have your consent to store the data?".encode())
	
	consent = connection.recv(BUFFER_SIZE)
	print(consent)


	if(consent):
		storage.store(response, data)

connection.close()
