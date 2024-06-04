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

        for order in transformed_order_data:
            date = order["order_date"]
            cursor.execute(date_query, (date,))
            date_id = cursor.fetchone()
            print(date_id[0])

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