import requests as req
import json
from bs4 import BeautifulSoup as bs

# Raw dir
USER_DATA_DIR = fr"data\raw"

# Random user API url
url = fr"https://randomuser.me/api/?results=50&inc=name,location,email,login,phone&nat=no&noinfo"

def get_resp(url):
    """Get response from url."""

    return req.get(url)


def save_to_json(dir_, filename, data):
    """Save json file to directory."""

    with open(fr'{dir_}\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_user_data(resp):

    user_data = []

    for person in resp.json()["results"]:
        person_d = {
            "first_name": person["name"]["first"],
            "last_name": person["name"]["last"],
            "address": person["location"]["street"]["name"] + " " + str(person["location"]["street"]["number"]),
            "city": person["location"]["city"],
            "state": person["location"]["state"],
            "zip": person["location"]["postcode"],
            "email": person["email"],
            "password": person["login"]["password"],
            "mobile_num": person["phone"]
        }

        user_data.append(person_d)

    return user_data


def generate_customers():

    resp = get_resp(url)
    user_data = get_user_data(resp)
    save_to_json(USER_DATA_DIR, "customer_data", user_data)