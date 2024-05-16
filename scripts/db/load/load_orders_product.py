import json
import psycopg2
import os
import random

os.sys.path.append('scripts')
from util.utils import connect_db

def extract_product_ids():

    try:
        conn = connect_db('komplett')
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


def clean_ids():

    product_id_rows = extract_product_ids()
    product_ids = [x[0] for x in product_id_rows]

    return product_ids


def generate_orders_product_rows():

    product_ids = clean_ids()
    num_orders = range(1, 101)
    # print(product_ids)

    out = []

    for order_id in num_orders:
        product_ids_set = set()
        num_products = random.randint(1, 10)

        while len(product_ids_set) < num_products:
            product_ids_set.add(random.choice(product_ids))
            

        for id_ in product_ids_set:
            product_quantity = random.randint(1, 10)
            out.append((product_quantity, order_id, id_))

    return out

a = generate_orders_product_rows()


def load_orders_product():

    rows = generate_orders_product_rows()

    try:
        conn = connect_db('komplett')
        cursor = conn.cursor()

        query = """
            INSERT INTO orders_product (quantity, orders_id, product_id)
            VALUES (%s, %s, %s);
            """
        
        for row in rows:
            cursor.execute(query, row)
    
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

# load_orders_product()
