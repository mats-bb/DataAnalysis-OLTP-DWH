import psycopg2
import os
from psycopg2.extras import RealDictCursor

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = r"extracted_order_data.json"

def extract_order_data():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT op.product_id, p.product_name, op.discount_id AS discount_id, o.payment_method, do2."type" AS delivery_method, do2.price AS delivery_price, op.quantity,
            ph.price AS regular_unit_price, o.order_date::text,
            d.discount_type, d.amount AS discount_amount, a.id AS location_id, o.customer_id as customer_id
            FROM orders_product op
            JOIN product p ON op.product_id = p.id 
            JOIN price_history ph ON op.product_id = ph.product_id
            JOIN orders o ON op.orders_id = o.id
            JOIN delivery_option do2 ON o.delivery_option_id = do2.id
            JOIN product_category pc ON p.product_cat_id  = pc.id
            JOIN type_category tc ON pc.type_cat_id = tc.id
            JOIN main_category mc ON tc.main_cat_id = mc.id
            JOIN customer c ON o.customer_id = c.id
            JOIN customer_address ca ON c.id = ca.customer_id
            JOIN address a ON ca.address_id = a.id
            JOIN city c2 ON a.city_id = c2.id
            JOIN discount d ON op.discount_id = d.id;
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

    save_to_json(EXTRACTED_DIR, FILE_NAME, rows)

extract_order_data()