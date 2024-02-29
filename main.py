import threading
import socket
import re
import Servidor, Cliente, config_file

def main():
    config_file.create_config_file()

    bootsp = input()
    
    while validar_ip(bootsp) == False:
        print("Invalid IP, try again:")
        bootsp = input()

    print("Connecting to the server...")
    connect_to_bootsp(bootsp)

    client = threading.Thread(target=Cliente.main)  
    server = threading.Thread(target=Servidor.main)
    
    client.start()
    server.start()

def validar_ip(ip):
    patron = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    if re.match(patron, ip):
        return True
    else:
        return False
    
def connect_to_bootsp(ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = config_file.get_port_server()
    server.connect((ip, port))
    

if __name__ == "__main__":
    main()