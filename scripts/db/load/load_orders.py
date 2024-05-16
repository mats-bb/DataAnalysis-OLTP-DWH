import json
import psycopg2
import os
import random
import pandas as pd

os.sys.path.append('scripts')
from util.utils import connect_db

def generate_customer_ids():

    customer_ids = set()

    while len(customer_ids) < 100:
        customer_ids.add(random.randint(1, 100))

    return list(customer_ids)


def generate_ips():
    
    ips = set()

    while len(ips) < 100:
        ips.add(f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}")

    return list(ips)


def generate_payment_method():
    
    payment_types = ["Card", "Invoice", "Special"]

    return random.choice(payment_types)


def generate_delivery_note():
    
    return "Test"


def generate_delivery_option():

    return random.randint(1, 3)


def generate_date():

    start_date = pd.to_datetime('2024-05-01')
    end_date = pd.to_datetime('2024-05-31')

    random_date = pd.to_datetime(random.choice(pd.date_range(start_date, end_date)))

    return random_date.strftime('%Y-%m-%d')


def generate_orders():

    customer_ids = generate_customer_ids()
    ips = generate_ips()

    orders = []

    for idx, id_ in enumerate(customer_ids):
        order = {
            "order_date": generate_date(),
            "ip_address": ips[idx],
            "payment_method": generate_payment_method(),
            "delivery_note": generate_delivery_note(),
            "delivery_option_id": generate_delivery_option(),
            "customer_id": id_
        }

        orders.append(order)

    return orders

def load_data():
    """Load data into database."""

    orders = generate_orders()

    try:
        conn = connect_db('komplett')
        cursor = conn.cursor()

        query = """
                INSERT INTO orders (order_date, ip_address, payment_method,
                           delivery_note, delivery_option_id, customer_id)
                VALUES(%s, %s, %s, %s, %s, %s)"""

        for order in orders:
            
            cursor.execute(query, [order[key] for key in order.keys()])

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

load_data()