import threading
import socket
import os
import config_file
import json

class Server:
    def __init__(self):
        self.ip = config_file.get_ip()
        self.port = config_file.get_port_server()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 1024
        self.tuple_connection = (self.ip, self.port)

        self.server_socket.bind(self.tuple_connection)
        self.server_socket.listen()

        print(f"Server running on {self.ip}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            thread_client = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread_client.start()

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")

        try:
            while True:
                data = client_socket.recv(self.buffer).decode()

                while data == "":
                    data = client_socket.recv(self.buffer).decode()

                data = json.loads(data)
                file_name = data['file_name']
                if self.search_file(file_name):
                    print(f"File {file_name} found")
                else:
                    print(f"File {file_name} not found")

        except ConnectionResetError:
            print(f"Connection from {address} was closed")

    def search_file(self, file):

        if file in os.listdir(config_file.get_directory()):
            return True
        
        return False

        

def main():
    Server()