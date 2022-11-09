
import socket
import datetime
import asyncio
from galileopass.server import create_server
HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 2424  # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("server listening ...")
    client, addr = s.accept()
    with client:
        print(f"Connected by {addr}")
        while True:
            data = client.recv(1024)
            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} - DATA ({len(data)} bytes)")
            print(f"{data}")
            # b = [a for a in data]
            # print(f'    dec -> {b}, len={len(b)}')
            bx = data.hex(sep=',')
            print(f'    hex -> {bx}, len={len(data)}')
            if not data:
                break
            pack_checksum = data[-2:]
            confirmation_header = b'\x02'
            confirmation_pack = confirmation_header + pack_checksum
            print(f"    confirmation: {confirmation_pack}\n")
            client.sendall(confirmation_pack)