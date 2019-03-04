import logging
import time

import requests

ip = requests.get('https://domains.google.com/checkip')


def start(username, password, domain, interval):
    while True:
        updatedomain(username, password, domain, ip)
        while ipcheck():
            time.sleep(interval)


def ipcheck():
    global ip
    newip = requests.get('https://domains.google.com/checkip')

    if ip == newip.content:
        logging.info('IP address unchanged, going to sleep')
        return ip
    else:
        logging.info('IP address changed from ' + ip.text + ' to ' + newip.text + ', updating . . .')
        ip = newip.content
        return ip


def updatedomain(username, password, domain, ip):
    userpass = username + ':' + password
    url = 'https://' + userpass + '@domains.google.com/nic/update?hostname=' + domain + "&myip=" + ip.text
    print(url)

    return requests.get(url)
