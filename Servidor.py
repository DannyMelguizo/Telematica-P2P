import threading
import socket
import config_file

class Server:
    def __init__(self):
        self.ip = config_file.get_ip()
        self.port = config_file.get_port_server()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 1024

        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

        print(f"Server running on {self.ip}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")

        while True:
            None

def main():
    Server()