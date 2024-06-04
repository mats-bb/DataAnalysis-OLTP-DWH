import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = "extracted_product_data.json"

def load_product_data():
    """Load data into database."""

    extracted_product_data = load_from_json(EXTRACTED_DIR, "extracted_product_data.json")

    try:
        conn = connect_db('komplett_v2_dwh')
        cursor = conn.cursor()

        query = """INSERT INTO dim_product (id, product_sku_number, product_mpn_number, product_name,
                           product_category, product_type_category, product_main_category, product_producer_name)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        for product in extracted_product_data:

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

load_product_data()