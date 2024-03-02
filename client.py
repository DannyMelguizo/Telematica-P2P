import socket
import os
import config_file

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


def main():
    pass


