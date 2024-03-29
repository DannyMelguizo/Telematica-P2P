import threading
import socket
import os
import grpc
import config_file, log_file, client, peers_file, transfer_files
import service_pb2, service_pb2_grpc
import json

from concurrent import futures

class Server:
    def __init__(self, is_bootsp):
        self.my_ip = config_file.get_ip()
        self.ip = '0.0.0.0'
        self.port = config_file.get_port_server()
        #Create the socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 1024

        if is_bootsp:
            grpc_thread = threading.Thread(target=self.server_grpc)
            grpc_thread.start()

        self.server_socket.bind((self.ip, self.port))  
        self.server_socket.listen()

        while True:
            client_socket, address = self.server_socket.accept()
            thread_client = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread_client.start()

    def server_grpc(self):
        peers_file.create_peers_file()
        port_grpc = config_file.get_port_grpc()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_GetAvailablePeersServicer_to_server(GetAvailablePeers(), server)
        server.add_insecure_port(f'[::]:{port_grpc}')
        server.start()
        server.wait_for_termination()


    def handle_client(self, client_socket, address):
        print("Connection from", address)
        if address[0] not in client.connections:
            client.connections.append(address[0])
        while True:
            data = client_socket.recv(self.buffer)

            if data:

                if data.decode().startswith("disconnect"):
                    data = data.decode().split(',')
                    father = data[1]
                    random_peer = data[2]

                    if address[0] == client.connections[0]:
                        if self.my_ip != random_peer:
                            client.connections[0] = random_peer
                        else:
                            client.connections[0] = father
                    else:
                        client.connections.remove(address[0])
                        if random_peer != "None" and random_peer not in client.connections and random_peer != self.my_ip:
                            client.connections.append(random_peer)

                    break

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

    def search_file(self, file):

        if file in os.listdir(config_file.get_directory()):
            return True
        
        return False
    
    def send_file(self, file, origin):
        data = {
            self.my_ip: file
        }

        json_data = json.dumps(data)
        data_bytes = json_data.encode()

        #Send the file to the origin
        transfer_files.upload_file(origin, data_bytes)

class GetAvailablePeers(service_pb2_grpc.GetAvailablePeersServicer):

    def AddIP(self, request, context):
        #Get a random ip from the server
        ip = peers_file.get_random_ip()
        #Add the new peer to the server
        peers_file.add_peer(ip, request.ip)

        #Return the ip to the client
        return service_pb2.IPResponse(ip=ip)

def main(is_bootsp = False):
    Server(is_bootsp)