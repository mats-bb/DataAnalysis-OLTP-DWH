import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import load_from_json, connect_db

TRANSFORMED_DIR = r"data\dwh\transformed"
FILE_NAME = "transformed_order_data.json"

def load_order_data():
    """Load data into database."""

    transformed_order_data = load_from_json(TRANSFORMED_DIR, FILE_NAME)

    try:
        conn = connect_db('komplett_v2_dwh')
        cursor = conn.cursor()

        date_query = """
            SELECT id 
            FROM dim_date
            WHERE date = %s;
            """

        query = """
            INSERT INTO fact_product_sale (product_id, discount_id, payment_method, delivery_method, quantity, regular_unit_price, location_id, customer_id,
                                            discount_unit_price, net_unit_price, extended_sales_amount, extended_discount_amount, date_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        for order in transformed_order_data:
            date = order["order_date"]
            cursor.execute(date_query, (date,))
            date_id = cursor.fetchone()
            order["date_id"] = date_id[0]
            del order["order_date"]
            # print(order)
            cursor.execute(query, tuple(order.values()))

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