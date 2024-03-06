import threading
import re
import grpc
import server, client, config_file, log_file, service_pb2, service_pb2_grpc

def main():
    config_file.create_config_file()
    log_file.create_log_file()

    print("Enter the IP of the Bootstrap Server:")
    bootsp = input()

    if bootsp != "Bootsp":
        #Verify if the ip given is valid and try to connect to the server
        peer_to_connect = try_connection(bootsp)
        client.connect_to_peer(peer_to_connect.ip)
        _server = threading.Thread(target=server.main)

    else:
        is_bootsp = True
        _server = threading.Thread(target=server.main, args=(is_bootsp,))

    try:  
        _client = threading.Thread(target=client.main)
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
    
    _client.start()
    _server.start()

def validate_ip(ip):
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    if ip == "0.0.0.0":
        return False

    #Verify if the ip given is valid
    if re.match(pattern, ip):
        return True
    else:
        return False
    
def try_connection(ip):

    peer_to_connect = None

    while validate_ip(ip) == False:
        print("Format IP invalid, try again:")
        ip = input()

    try:
        print("Connecting to the server...")
        #Connect to the server bootsp
        peer_to_connect = connect_to_bootsp(ip)

    except Exception as e:
        print("An error has ocurred connection to the server\nTry another IP:")
        
        log = f"Error trying to connect to the server {ip}"
        log_file.write_log_file(log, 2)

        ip = input()
        peer_to_connect = try_connection(ip)
    
    return peer_to_connect

    
def connect_to_bootsp(ip):
    port = config_file.get_port_grpc()
    my_ip = config_file.get_ip()

    #Connection with gRPC to the server in gRPC port
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = service_pb2_grpc.GetAvailablePeersStub(channel)

        #The IP answered by the server is added to the list of peers
        response = stub.AddIP(service_pb2.IPAddressClient(ip=my_ip))

        return response
        

if __name__ == "__main__":
    main()
    