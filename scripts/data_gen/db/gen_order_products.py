import psycopg2
import os
import random

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

DATA_GEN_PATH = r"data\data_gen"


def extract_product_ids():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT id from product;
            """
        
        cursor.execute(query)
        rows = cursor.fetchall()

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


def extract_order_ids():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT id from orders;
            """
        
        cursor.execute(query)
        rows = cursor.fetchall()

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


def clean_ids(func):

    product_id_rows = func
    product_ids = [x[0] for x in product_id_rows]

    return product_ids


def generate_orders_product_rows():

    product_ids = clean_ids(extract_product_ids())
    # num_orders = range(NUM_ORDERS)
    order_ids = clean_ids(extract_order_ids())

    order_products_rows = []

    # for order_id in num_orders:
    for order_id in order_ids:
        product_ids_set = set()
        num_products = random.randint(1, 10)

        while len(product_ids_set) < num_products:
            product_ids_set.add(random.choice(product_ids))
            
        for product_id in product_ids_set:
            product_quantity = random.randint(1, 10)
            order_products_rows.append((product_quantity, order_id, product_id))

    save_to_json(DATA_GEN_PATH, "order_products.json", order_products_rows)

generate_orders_product_rows()