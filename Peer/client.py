import socket
import config_file, log_file, transfer_files
import json
import random
import threading

connections = []
list_files = []

def Interface():
    global list_files
    print("\nSelect a number to navigate through the menu.")
    print("1. Search for a file")
    print("2. List all connections\n")
    print("0. Exit\n")
    option = input()
    
    try:
        int(option)
    except:
        print("Invalid option\n")
        Interface()

    if int(option) == 0:
        disconnect()

    elif int(option) == 1:
        print("Enter the name of the file you are looking for:")
        file = input()

        data = {
            "file_name": file,
            "origin": config_file.get_ip(),
            "last_peer": config_file.get_ip()
        }

        list_files = []
        print("Looking for the file...\n\nIf the file is found, we will show you a list below.\n")
        print("Press any key to go back to the menu.")

        threading.Thread(target=transfer_files.get_file).start()

        #Send the request to the known peers
        send_request(data)
        
        option = input()
        Interface()


    elif int(option) == 2:
        print("Connections:")
        for i in connections:
            print(i)

        Interface()

    else:
        print("Invalid option\n")
        Interface()

def show_files_found():
    print("\nFiles found:")
    files = enumerate(list_files)
    for idx, file in files:
        file = json.loads(file)
        print(f"{idx+1}. {list(file.keys())[0]} {list(file.values())[0]}")
    
    print("\nPress any key to go back to the menu.")
    option = input()
    Interface()

def connect_to_peer(ip):
    #Create the socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, config_file.get_port_server()))
    client_socket.close()

    log = f"Connected to {ip}"
    log_file.write_log_file(log, 1)
    connections.append(ip)

def files_founds(data):
    list_files.append(data)
    show_files_found()

def send_request(data):
    #Send the request to the known peers
    for i in connections:
        if i == data['last_peer']:
            continue
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((i, config_file.get_port_server()))
        client_socket.send(json.dumps(data).encode())
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()

def disconnect():
    print("\nDisconnecting...")

    father = connections[0]
    try:
        random_peer = connections[random.randint(1, len(connections)-1)]
    except:
        random_peer = None

    for i in connections:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((i, config_file.get_port_server()))
        client_socket.send(f"disconnect,{father},{random_peer}".encode())
        client_socket.close()
    
    log = f"Disconnecting"
    log_file.write_log_file(log, 1)

    print("To exit, press Ctrl+C\n")

def main():
    Interface()
