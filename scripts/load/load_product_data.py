import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

RAW_DIR = fr"data\raw"


# Remake the stored procedure to handle jsonb input instead of this solution
def load_data():
    """Load data into database."""

    products = load_from_json(RAW_DIR, "combined_product_data")

    try:
        conn = connect_db()
        cursor = conn.cursor()

        for product in products:
            d = {
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

            # Call the stored procedure with unpacked values
            cursor.execute("CALL insert_product_data(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", [d[key] for key in d.keys()])

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