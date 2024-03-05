import config_file
import json
import random

def create_pears_file():
    ip = config_file.get_ip()

    pears = {
        'pears_available': {}
    }

    pears['pears_available'][ip] = []

    with open('pears.json', 'w') as file:
        json.dump(pears, file)

def get_pears():
    with open('pears.json', 'r') as file:
        pears = json.loads(file.read())
    return pears

def get_random_ip():
    available_pears = get_pears()['pears_available']
    ips = list(available_pears.keys())

    randomip = ips[random.randint(0, len(ips)-1)]

    #Verify if the random ip has less than 2 pears // The maximum number of pears is 3
    while len(available_pears[randomip]) >= 2:
        randomip = ips[random.randint(0, len(ips)-1)]

    return randomip

def add_pear(ip_father, ip_son):
    pears = get_pears()

    #Add the new pear to his father
    pears['pears_available'][ip_father].append(ip_son)
    #Link the new pear with his father
    pears['pears_available'][ip_son] = [ip_father]

    with open('pears.json', 'w') as file:
        json.dump(pears, file)
