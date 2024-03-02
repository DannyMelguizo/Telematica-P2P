import threading
import re
import grpc
import server, client, config_file, log_file, service_pb2, service_pb2_grpc

def main():
    config_file.create_config_file()
    log_file.create_log_file()

    print("Enter the IP of the Bootstrap Server:")
    bootsp = input()
    
    while validate_ip(bootsp) == False:
        print("Format IP invalid, try again:")
        bootsp = input()

    print("Connecting to the server...")
    connect_to_bootsp(bootsp)
    config_file.setPear(bootsp)

    _client = threading.Thread(target=client.main)  
    _server = threading.Thread(target=server.main)
    
    _client.start()
    _server.start()

def validate_ip(ip):
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    #Verify if the ip given is valid
    if re.match(pattern, ip):
        return True
    else:
        return False
    
def connect_to_bootsp(ip):
    port = config_file.get_port_grpc()

    with grpc.insecure_channel(ip + ":" + port) as channel:
        stub = service_pb2_grpc.GetAvailablePearsStub(channel)
        response = stub.AddIP(service_pb2.IPAddressClient(ip=ip))
        print(f'szs {response.message}')

    

if __name__ == "__main__":
    main()