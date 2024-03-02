import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("190.70.144.217", 8000))

data = {
    "origin": "Pear1",
    "file_name": "file.txt"
}

s.send(json.dumps(data).encode())
