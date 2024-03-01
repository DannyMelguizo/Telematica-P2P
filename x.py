import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.1.65", 9999))

data = {
    "origin": "Pear1",
    "file_name": "file.txt"
}

s.send(json.dumps(data).encode())
