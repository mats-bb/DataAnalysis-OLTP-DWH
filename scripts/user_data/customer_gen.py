# Generate customer profiles 
# First name, optional midle name, last name, email, password, mobile number

# Address information


# API for name generation? 
# API for address generation?
# API for email generation?

import requests as req
import json

USER_DATA_DIR = fr"scripts\user_data"

url = fr"https://randomuser.me/api/?results=50&inc=name,location,email,login,phone&nat=no&noinfo"

res = req.get(url)

def save_to_json(dir_, filename, data):
    """Save json file to directory."""

    with open(fr'{dir_}/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

people = []

for person in res.json()["results"]:
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

    people.append(person_d)

save_to_json(USER_DATA_DIR, "customer_data", people)