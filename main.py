import threading
import re
import server, cliente, config_file, log_file

def main():
    config_file.create_config_file()
    log_file.create_log_file()

    print("Enter the IP of the Bootstrap Server:")
    bootsp = input()
    
    while validate_ip(bootsp) == False:
        print("Format IP invalid, try again:")
        bootsp = input()

    print("Connecting to the server...")
    #connect_to_bootsp(bootsp)
    config_file.setPear(bootsp)

    _client = threading.Thread(target=cliente.main)  
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
    port = config_file.get_port_server()

    

if __name__ == "__main__":
    main()