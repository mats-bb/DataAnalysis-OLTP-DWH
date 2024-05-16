import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db


def extract_products():

    try:
        conn = connect_db('komplett')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, pi2.sku, pi2.mpn, p.product_name, pc.category_name, tc.category_name, mc.category_name, p2.producer_name 
            FROM product p
            JOIN product_category pc ON
            p.product_cat_id = pc.id
            JOIN type_category tc ON
            pc.type_cat_id = tc.id 
            JOIN main_category mc ON
            tc.main_cat_id = tc.id
            JOIN product_inventory pi2 ON
            p.id = pi2.product_id
            JOIN producer p2 ON 
            p.producer_id = p2.id;
        """)

        rows = cursor.fetchall()

    except psycopg2.Error as e:
        print("Error:", e)

    finally:

        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows



def load_data():
    """Load data into database."""

    product_data = extract_products()

    try:
        conn = connect_db('komplett_dwh')
        cursor = conn.cursor()

        query = """INSERT INTO dim_product (id, product_sku_number, product_mpn_number, product_name,
                           product_category, product_type_category, product_main_category, product_producer_name)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        for product in product_data:

            cursor.execute(query, product)

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
