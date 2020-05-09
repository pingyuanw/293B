import socket

TCP_IP = "1"
TCP_PORT = 5555
BUFFER_SIZE = 1024

data = input("Enter your features: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send(data)
response = sock.recv(BUFFER_SIZE)
assert(response == data)
print("edge received data.")

ask = sock.recv(BUFFER_SIZE)
print(ask)

consent = input("Enter your 1 for yes or 0 for no: ")
sock.send(consent)

infer = s.recv(BUFFER_SIZE)
print("infered: "+str(infer))
s.close()