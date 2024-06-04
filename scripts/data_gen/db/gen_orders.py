import os
import random
import pandas as pd
import random
from datetime import datetime, timedelta

os.sys.path.append('scripts')
from util.utils import save_to_json, load_from_json

DATA_GEN_PATH = r"data\data_gen"
YEAR = 2024
START_DATE = "01-01"
END_DATE = "05-20"
NUM_ORDERS = 3500


def get_customer_id_date():

    customer_data = load_from_json(DATA_GEN_PATH, "combined_customer_data.json")

    customer_ids_dates = []

    for idx, customer_data in enumerate(customer_data):
        customer_id = idx+1
        account_created_date = customer_data["account_created_date"]
        id_date = (customer_id, account_created_date)
        customer_ids_dates.append(id_date)

    return customer_ids_dates


def generate_ips():
    
    ips = set()

    while len(ips) < NUM_ORDERS:
        ips.add(f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}")

    return list(ips)


def generate_payment_method():
    
    payment_types = ["Card", "Invoice", "Payment Plan"]

    return random.choice(payment_types)


def generate_delivery_note():
    
    return "Test"


def generate_delivery_option():

    return random.randint(1, 3)


def parse_date(date_str, date_format="%Y-%m-%d"):

    return datetime.strptime(date_str, date_format)


def generate_date_range(start_date, end_date):

    date_range = []
    current_date = start_date

    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)

    return date_range


def generate_orders():

    customer_ids_dates = get_customer_id_date()
    ips = generate_ips()
    start_date = datetime.strptime(f"{YEAR}-{START_DATE}", "%Y-%m-%d")
    end_date = datetime.strptime(f"{YEAR}-{END_DATE}", "%Y-%m-%d")

    all_dates = generate_date_range(start_date, end_date)

    orders = []

    for ip in ips:
        customer_id_account_created_date = random.choice(customer_ids_dates)
        customer_id = customer_id_account_created_date[0]
        customer_created_date = parse_date(customer_id_account_created_date[1])
        

        valid_dates = []
        for date in all_dates:
            if date >= customer_created_date:
                valid_dates.append(date)

        if not valid_dates:
            continue
        
        order_date = str(random.choice(valid_dates).date())

        order = {
            "order_date": order_date,
            "ip_address": ip,
            "payment_method": generate_payment_method(),
            "delivery_note": generate_delivery_note(),
            "delivery_option_id": generate_delivery_option(),
            "customer_id": customer_id
        }

        orders.append(order)

    save_to_json(DATA_GEN_PATH, f"orders_{YEAR}.json", orders)

generate_orders()