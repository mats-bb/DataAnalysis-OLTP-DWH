import psycopg2
from psycopg2.extras import RealDictCursor
import os
from decimal import Decimal
from datetime import date

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = fr"data\extracted"

def convert_types(row):
    for key, value in row.items():
        if isinstance(value, Decimal):
            row[key] = float(value)
        elif isinstance(value, date):
            row[key] = value.isoformat()
    return row


def extract_orders():

    try:
        conn = connect_db('komplett')
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT op.product_id, d.id AS discount_id, o.payment_method, do2."type" AS delivery_method, do2.price AS delivery_price, op.quantity,
            ph.price AS regular_unit_price, o.order_date,
            d.discount_type, d.amount AS discount_amount, a.zip_code, c2.city_name 
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
            LEFT JOIN product_discount pd ON op.product_id = pd.product_id
            LEFT JOIN discount d ON pd.discount_id = d.id
            ORDER BY op.product_id;
            """

        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    except psycopg2.Error as e:
        print(e)

    finally:

        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return rows


def clean_data():

    rows = extract_orders()
    clean_rows = []

    for row in rows:
        clean_row = convert_types(row)
        clean_rows.append(clean_row)

    save_to_json(EXTRACTED_DIR, "extracted_orders", clean_rows)

clean_data()
