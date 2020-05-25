#communicate with client
import socket
import sys
import storage
import inference


TCP_IP = '127.0.0.1'#localhost
TCP_PORT = 5000
BUFFER_SIZE = 1024

aws_access_key_id='Secret'
aws_secret_access_key='Secret'


inference_handler = inference.Inference(aws_access_key_id, aws_secret_access_key)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
connection, client_address = sock.accept()

while(1):
	data = []
	msg = connection.recv(BUFFER_SIZE)
	while(msg!="done sending the image".encode()):
		data += msg
		msg= connection.recv(BUFFER_SIZE)
	
	print("received msg: "+str(msg))
	
	connection.send("do we have your consent to store the data?".encode())
	
	consent = connection.recv(BUFFER_SIZE)
	print(consent)

	response = inference_handler.predict(data)

	if(consent):
		storage.store(response, data)

	
	connection.send(bytes(response))

connection.close()
