#communicate with client
import socket
import sys
import storage
import inference

TCP_IP = 'localhost'
TCP_PORT = 5555
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
connection, client_address = sock.accept()
while(1):
	data = connection.recv(BUFFER_SIZE)
	if not data: break
	print("received data: "+str(data))
	connection.send(data)
	
	storage.store(data)
	response = infer(data)
	
	connection.send(response)
connection.close()
