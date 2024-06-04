import grequests
import os
import pandas as pd
import random

os.sys.path.append('scripts')
from util.utils import save_to_json


USER_DATA_DIR = fr"data\data_gen"
NUM_CUSTOMERS = 5000
SEEDS = list(range(1, 5))

START_DATE = "2022-01-01"
END_DATE = "2022-12-31"

# Random user API url
# URL = fr"https://randomuser.me/api/?results={NUM_CUSTOMERS}&{seed}&inc=name,location,email,login,phone&nat=no&noinfo"

def generate_account_created_date():

    start_date = pd.to_datetime(f'{START_DATE}')
    end_date = pd.to_datetime(f'{END_DATE}')

    random_date = pd.to_datetime(random.choice(pd.date_range(start_date, end_date)))

    return random_date.strftime('%Y-%m-%d')


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
            "mobile_num": person["phone"],
            "account_created_date": generate_account_created_date()
        }
        dob_full = person["dob"]["date"]
        dob_date = dob_full[:dob_full.find("T")]
        person_d["DOB"] = dob_date

        user_data.append(person_d)

    return user_data


def remove_duplicates_by_keys(dicts_list, keys_to_check):
    seen_values = set()
    unique_dicts = []

    for d in dicts_list:
        duplicate_found = False

        for key in keys_to_check:
            if key in d:
                value = d[key]

                if value in seen_values:
                    duplicate_found = True
                    break
                seen_values.add(value)
        
        if not duplicate_found:
            unique_dicts.append(d)

    return unique_dicts


def generate_customers():

    customers = []

    urls = [fr"https://randomuser.me/api/?results={NUM_CUSTOMERS}&seed={seed}&inc=name,location,email,login,phone,dob&nat=no&noinfo" for seed in SEEDS]

    async_requests = [grequests.get(url) for url in urls]
    responses = grequests.map(async_requests)

    for resp in responses:
        print(resp.status_code)
        if resp.status_code == 200:
            user_data = get_user_data(resp)
            customers.extend(user_data)
        else:
            pass

    filtered_customers = remove_duplicates_by_keys(customers, ["email", "mobile_num"])
    save_to_json(USER_DATA_DIR, "customer_data.json", filtered_customers)

generate_customers()