import socket

TCP_IP = '127.0.0.1'#localhost
TCP_PORT = 5000
BUFFER_SIZE = 1024

data = input("Enter your features: ")
data=data.encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send(data)

ask = sock.recv(BUFFER_SIZE)
print(ask)

consent = input("Enter your 1 for yes or 0 for no: ")
sock.send(consent.encode())

infer = sock.recv(BUFFER_SIZE)
infer = int.from_bytes(infer,byteorder='big')
print("infered: "+str(infer))
sock.close()
