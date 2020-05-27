import socket
import os
import sys
from struct import *


TCP_IP = '127.0.0.1'#localhost
TCP_PORT = 5000
BUFFER_SIZE = 1024

filename = input("Enter your image file name: ")

try:
	f = open(filename, 'rb')
except:
	print("file not exist")

filesize = str(os.path.getsize(filename))
print("file size is: "+str(filesize))
data=f.read(BUFFER_SIZE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

filesize = pack('!I', int(filesize))
sock.send(filesize)

while(data):
	print("Sending...")
	sock.send(data)
	data=f.read(BUFFER_SIZE)
f.close()

print("done sending file ...")

rsp_size = sock.recv(4)
rsp_size = unpack('!I', rsp_size)[0]

infer = sock.recv(rsp_size )
infer = infer.decode('utf-8')
print("infered: "+str(infer))

ask = sock.recv(BUFFER_SIZE)
print(ask)

consent = input("Enter your 1 for yes or 0 for no: ")

sock.send(consent.encode())

sock.close()
