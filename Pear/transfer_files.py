import config_file, client
import socket
import threading


class Server():
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = config_file.get_port_mom()
        self.buffer = 1024

        self.recv_files = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_files.bind((self.ip, self.port))
        self.recv_files.listen()

        while True:
            client_file, address = self.recv_files.accept()
            thread_client_file = threading.Thread(target=self.handle_client, args=(client_file, address))
            thread_client_file.start()

    def handle_client(self, client_socket, address):
        try:
            while True:
                data = client_socket.recv(self.buffer)

                if data:
                    data = data.decode()
                    client.files_founds(data)

                    client_socket.close()
                    break

        except ConnectionResetError:
            print(f"Connection from {address} was closed")


def main():
    Server()