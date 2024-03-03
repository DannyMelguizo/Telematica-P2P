import socket
import config_file, log_file
import json

connections = []

def Interfaz():
    print("Select a number to navigate through the menu.")
    print("1. Search for a file")
    print("2. List all connections")
    print("0. Exit")
    option = int(input())

    if option == 1:
        print("\nEnter the name of the file you are looking for:")
        file = input()

        data = {
            "file_name": file,
            "origin": config_file.get_ip(),
            "last_peer": config_file.get_ip()
        }

        #Send the request to the known peers
        send_request(data)
        print("waiting for response...")


    elif option == 2:
        print("Connections:")
        for i in connections:
            print(i)

        print("\n")
        Interfaz()

    elif option == 0:
        pass

def connect_to_peer(ip):
    #Create the socket
    port = config_file.get_port_server()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.close()

    log = f"Connected to {ip}"
    log_file.write_log_file(log, 1)
    connections.append(ip)

def send_request(data):
    print(connections)
    port = config_file.get_port_server()
    #Send the request to the known peers
    for i in connections:
        if i == data['last_peer']:
            continue
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((i, port))
        client_socket.send(json.dumps(data).encode())
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()


def main():
    Interfaz()
