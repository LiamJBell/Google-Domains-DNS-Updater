import json
import logging

import ipchanger


def main():
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s: %(message)s')

    with open('credentials.json') as file:
        data = json.load(file)

    user = data["credentials"][0]["user"]
    password = data["credentials"][0]["pass"]
    domain = data["credentials"][0]["domain"]
    interval = 3600  # the update interval
    ipchanger.start(user, password, domain, interval)


if __name__ == '__main__':
    main()
