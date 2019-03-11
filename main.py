import logging
from json import loads as json_loads
from sys import exit
from time import sleep

import requests


def _load_credentials(filename: str) -> tuple:
    with open(filename) as file:
        data = json_loads(file.read())
    return data["username"], data["password"], data["domain"]


def get_ip() -> str:
    return requests.get("https://domains.google.com/checkip").text


def update_ip(username: str, password: str, domain: str, new_ip: str) -> str:
    user_pass = username + ":" + password
    url = "https://" + user_pass + "@domains.google.com/nic/update?hostname=" + domain + "&myip=" + new_ip
    return requests.get(url).text


def main():
    logging.basicConfig(filename="dns-updater.log",
                        level=logging.INFO,
                        format="[%(asctime)-15s] [%(levelname)-8s] %(message)s")

    logging.log(logging.INFO, "Starting up service")

    logging.log(logging.INFO, "Loading credentials")
    username, password, domain = "", "", ""
    try:
        username, password, domain = _load_credentials("credentials.json")
    except Exception as e:
        logging.log(logging.CRITICAL, "Could not load credentials: " + str(e))
        exit(1)

    current_ip = get_ip()
    logging.log(logging.INFO, "Initial IP: " + current_ip)
    update_ip(username, password, domain, current_ip)

    internal_seconds = 120
    logging.log(logging.INFO, "Using interval of " + str(internal_seconds) + " seconds")
    while True:
        try:
            sleep(internal_seconds)
            check_ip = get_ip()
            if check_ip != current_ip:
                logging.log(logging.INFO, "IP has changed (%s) -> (%s), updating".format(current_ip, check_ip))
                current_ip = check_ip
                update_response = update_ip(username, password, domain, check_ip)
                logging.log(logging.INFO, "Response from IP update: " + update_response)
        except Exception as e:
            logging.log(logging.ERROR, "Exception occurred in main loop: " + str(e))


if __name__ == "__main__":
    main()
