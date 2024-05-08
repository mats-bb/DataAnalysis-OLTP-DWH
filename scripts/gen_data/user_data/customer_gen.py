import os

os.sys.path.append('scripts')
from util.utils import get_resp, save_to_json


# Raw dir
USER_DATA_DIR = fr"data\raw"

# Random user API url
url = fr"https://randomuser.me/api/?results=50&inc=name,location,email,login,phone&nat=no&noinfo"



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