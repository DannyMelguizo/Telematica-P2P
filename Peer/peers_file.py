import config_file
import json
import random

def create_peers_file():
    ip = config_file.get_ip()

    peers = {
        'peers_available': {}
    }

    peers['peers_available'][ip] = []

    with open('peers.json', 'w') as file:
        json.dump(peers, file)

def get_peers():
    with open('peers.json', 'r') as file:
        peers = json.loads(file.read())
    return peers

def get_random_ip():
    available_peers = get_peers()['peers_available']
    ips = list(available_peers.keys())

    randomip = ips[random.randint(0, len(ips)-1)]

    #Verify if the random ip has less than 2 peers // The maximum number of peers is 3
    while len(available_peers[randomip]) > 2:
        randomip = ips[random.randint(0, len(ips)-1)]

    return randomip

def add_peer(ip_father, ip_son):
    peers = get_peers()

    #Add the new peer to his father
    peers['peers_available'][ip_father].append(ip_son)
    #Link the new peer with his father
    peers['peers_available'][ip_son] = [ip_father]

    with open('peers.json', 'w') as file:
        json.dump(peers, file)
