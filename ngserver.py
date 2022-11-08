import socket

##ngrok tcp://0.tcp.sa.ngrok.io:13624

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 9999))

server.listen()

while True:
    client,addr = server.accept()
    client.send("Hello Worlds".encode())

    print(client.recv(1024).decode())
    client.close()
