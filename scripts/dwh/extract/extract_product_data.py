import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"

def extract_product_data():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT p.id, pi2.sku, pi2.mpn, p.product_name, pc.category_name AS product_category, tc.category_name AS type_category, mc.category_name AS main_category,
            p2.producer_name 
            FROM product p
            JOIN product_category pc ON p.product_cat_id = pc.id
            JOIN type_category tc ON pc.type_cat_id = tc.id
            JOIN main_category mc ON tc.main_cat_id = mc.id
            JOIN product_inventory pi2 ON p.id = pi2.product_id
            JOIN producer p2 ON p.producer_id = p2.id;
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

    save_to_json(EXTRACTED_DIR, "extracted_product_data.json", rows)

extract_product_data()