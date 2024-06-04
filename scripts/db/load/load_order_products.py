import psycopg2
import os


os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json, save_to_json

DATA_GEN_DIR = r"data\data_gen"
ORDER_PRODUCTS_FILE_NAME = "order_products.json"

def load_orders_product():
    """Load order_products data into the database."""

    rows = load_from_json(DATA_GEN_DIR, ORDER_PRODUCTS_FILE_NAME)

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        check_discount_query = """
            WITH date_cte AS (
            SELECT order_date
            FROM orders
            WHERE id = %s
            ),
            discount_dates AS (
                SELECT d.id, d.start_date, d.end_date
                FROM discount d
                JOIN discount_product dp ON d.id = dp.discount_id 
                WHERE dp.product_id = %s
            )
            SELECT dd.id
            FROM date_cte dc
            JOIN discount_dates dd ON dc.order_date BETWEEN dd.start_date AND dd.end_date; 
            """

        insert_query = """
            INSERT INTO orders_product (quantity, orders_id, product_id, discount_id)
            VALUES (%s, %s, %s, %s);
            """
        
        for row in rows:
            quantity, order_id, product_id = row
            cursor.execute(check_discount_query, (order_id, product_id))
            discount_id = cursor.fetchone()
            
            if not discount_id:
                discount_id = 1
            else:
                discount_id = discount_id[0]
            cursor.execute(insert_query, (quantity, order_id, product_id, discount_id))


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
    
load_orders_product()