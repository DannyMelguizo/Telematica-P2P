import socket
import config_file, log_file
import json

connections = []
list_files = []

def Interface():
    global list_files
    print("\nSelect a number to navigate through the menu.")
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
        list_files = []
        print("waiting for response...")


    elif option == 2:
        print("Connections:")
        for i in connections:
            print(i)

        Interface()

    elif option == 0:
        pass

def show_files_found():
    print("\nFiles found:")
    for idx, file in enumerate(list_files):
        file = json.loads(file)
        print(f"{idx+1}. {list(file.keys())[0]} {list(file.values())[0]}")
    

    Interface()

def connect_to_peer(ip):
    #Create the socket
    print(f"Connecting to {ip}")
    port = config_file.get_port_server()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.close()

    log = f"Connected to {ip}"
    log_file.write_log_file(log, 1)
    connections.append(ip)

def files_founds(data):
    list_files.append(data)
    show_files_found()

def send_request(data):
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
    Interface()
