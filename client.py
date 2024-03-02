import socket
import os
import config_file, log_file

def Interfaz():
    print("Select a number to navigate through the menu.")
    print("1. Search for a file")
    print("0. Exit")
    option = int(input())

    if option == 1:
        print("Enter the name of the file you are looking for:")
        file = input()
        #search_file(file)
    elif option == 0:
        pass

def connect_to_peer(ip):
    port = config_file.get_port_server()
    #Create the socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    log = f"Connected to {ip}"
    log_file.write_log_file(log, 1)

    return client_socket

def main():
    #Interfaz()
    pass


