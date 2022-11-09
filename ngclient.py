import socket
import time
TCP_IP = '52.87.243.230'
TCP_PORT = 2424
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
try:
    while True:
        s.send(MESSAGE.encode())
        data = s.recv(BUFFER_SIZE)
        print ("received data:", data)
        time.sleep(1)
except:
    print ("keyboard exception")
    s.close()