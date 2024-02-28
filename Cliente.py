import socket
import os
import configparser

config = configparser.ConfigParser()
bootp = ['first_server', "second_server"]

def create_config_file():
    ip = get_ip()
    name_directory = 'shared_files'

    #Create the folder where the files will be saved
    os.mkdir(name_directory)

    config['config'] = {
        'ip_public': f'{ip}',
        'port': '8080',
        'directory': f'{name_directory}',
    }

    #Create the file config.conf
    with open('config.conf', 'w') as archivo:
        config.write(archivo)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip

def conected_pears():
    None


if __name__ == "__main__":
    create_config_file()