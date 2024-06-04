import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

DATA_GEN_DIR = r"data\data_gen"
ORDER_FILE_NAME = "orders_2024.json"

def load_order_data():
    """Load order data into database."""

    orders = load_from_json(DATA_GEN_DIR, f"{ORDER_FILE_NAME}")

    try:
        conn = connect_db('komplett_v2_oltp')
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

load_order_data()