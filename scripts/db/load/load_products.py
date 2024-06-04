import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

TRANSFORMED_DIR = r"data\db\transformed"
PRODUCT_NAME = r"lagring"


# Remake the stored procedure to handle jsonb input instead of this solution
def load_product_data():
    """Load product data into database."""

    products = load_from_json(TRANSFORMED_DIR, f"transformed_{PRODUCT_NAME}_product_data.json")

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        for product in products:
            product_dict = {
                "main_category_name": product["categories"]["main_category"],
                "type_category_name": product["categories"]["type_category"],
                "product_category_name": product["categories"]["product_category"],
                "producer_name": product["producer"],
                "product_name": product["name"],
                "product_description": product["description"],
                "price": product["price"], 
                "specs": json.dumps(product["spec_sheet"]),
                "sku": product["sku"],
                "mpn": product["mpn"],
                "quantity": 0
            }
            product_json = json.dumps(product_dict)
            
            # Call the stored procedure with unpacked values
            cursor.execute("CALL insert_product_data(%s);", (product_json,))

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