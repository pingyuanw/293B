import socket

TCP_IP = "1"
TCP_PORT = 5555
BUFFER_SIZE = 1024

data = input("Enter your features: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
s.send(data)
response = s.recv(BUFFER_SIZE)
assert(response == data)
print("edge received data.")

infer = s.recv(BUFFER_SIZE)
print("infered: "+str(infer))
s.close()