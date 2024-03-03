import threading
import re
import grpc
import server, client, transfer_files,config_file, log_file, service_pb2, service_pb2_grpc

def main():
    config_file.create_config_file()
    log_file.create_log_file()

    print("Enter the IP of the Bootstrap Server:")
    bootsp = input()

    #Verify if the ip given is valid and try to connect to the server
    pear_to_connect = try_connection(bootsp)

    client.connect_to_peer(pear_to_connect.ip)
    
    _client = threading.Thread(target=client.main)  
    _server = threading.Thread(target=server.main)
    _transfer_files = threading.Thread(target=transfer_files.main)
    
    _client.start()
    _server.start()
    _transfer_files.start()

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

    pear_to_connect = None

    while validate_ip(ip) == False:
        print("Format IP invalid, try again:")
        ip = input()

    try:
        print("Connecting to the server...")
        #Connect to the server bootsp
        pear_to_connect = connect_to_bootsp(ip)

    except:
        print("Error connecting to the server\nTry another IP:")
        ip = input()
        pear_to_connect = try_connection(ip)
    
    return pear_to_connect

    
def connect_to_bootsp(ip):
    port = config_file.get_port_grpc()
    my_ip = config_file.get_ip()

    #Connection with gRPC to the server in gRPC port
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = service_pb2_grpc.GetAvailablePearsStub(channel)

        #The IP answered by the server is added to the list of peers
        response = stub.AddIP(service_pb2.IPAddressClient(ip=my_ip))

        return response
        

if __name__ == "__main__":
    main()