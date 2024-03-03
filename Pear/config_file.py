import os
import configparser
import requests

config = configparser.ConfigParser()

def create_config_file():
    ip = public_ip()
    name_directory = 'shared_files'
    proto_path = 'protobufs/service.proto'

    #Create the folder where the files will be saved
    try:
        os.mkdir(name_directory)
    except:
        print('The directory already exists')

    config['config'] = {
        'ip_public': f'{ip}',
        'port_server': '8000',
        'port_grpc': '9998',
        'port_mom': '9997',
        'port_rest': '9996',
        'directory': f'{name_directory}',
        'proto_path': f'{proto_path}'
    }

    #Create the file config.conf
    with open('config.conf', 'w') as archivo:
        config.write(archivo)

def public_ip():
    ip = requests.get("https://api.ipify.org").text
    return ip

def get_config():
    config.read('config.conf')

    return config

def get_ip():
    return get_config()['config']['ip_public']

def get_port_server():
    return int(get_config()['config']['port_server'])

def get_port_grpc():
    return int(get_config()['config']['port_grpc'])

def get_port_mom():
    return int(get_config()['config']['port_mom'])

def get_directory():
    return get_config()['config']['directory']

