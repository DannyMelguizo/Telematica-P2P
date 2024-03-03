import threading
import socket
import os
import config_file, log_file, client, transfer_files
import json

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = config_file.get_port_server()
        #Create the socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 1024

        self.server_socket.bind((self.ip, self.port))  
        self.server_socket.listen()

        while True:
            client_socket, address = self.server_socket.accept()
            thread_client = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread_client.start()

    def handle_client(self, client_socket, address):
        print("Connection from", address)
        if address[0] not in client.connections and len(client.connections) < 3:
            client.connections.append(address[0])
        try:
            while True:
                data = client_socket.recv(self.buffer)

                if data:

                    print(data)

                    data = json.loads(data)
                    file_name = data['file_name']
                    last_peer = address[0]
                    data['last_peer'] = last_peer
                    origin = data['origin']

                    log = f"{origin} requested {file_name} from {last_peer}"
                    log_file.write_log_file(log)

                    #Send the file
                    if self.search_file(file_name):
                        print(f"File {file_name} found")
                        self.send_file(file_name, origin)
            
                        client_socket.close()
                        break
                        
                    #Transfer the request to another peer
                    else:
                        print(f"File {file_name} not found")
                        print(f"Transfering request to another peer")
                        client.send_request(data)

                        client_socket.close()
                        break

        except ConnectionResetError:
            print(f"Connection from {address} was closed")

    def search_file(self, file):

        if file in os.listdir(config_file.get_directory()):
            return True
        
        return False
    
    def send_file(self, file, origin):
        my_ip = config_file.get_ip()
        port_mom = config_file.get_port_mom()
        data = {
            my_ip: file
        }
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((origin, port_mom))
        client_socket.send(json.dumps(data).encode())
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()

def main():
    Server()