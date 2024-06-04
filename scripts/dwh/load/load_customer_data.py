import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = r"extracted_customer_data.json"

def load_product_data():
    """Load data into database."""

    extracted_customer_data = load_from_json(EXTRACTED_DIR, FILE_NAME)

    try:
        conn = connect_db('komplett_v2_dwh')
        cursor = conn.cursor()

        query = """INSERT INTO Dim_customer (id, first_name, last_name, full_name,
                    date_of_birth, email, mobile_number, account_created_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""

        for customer in extracted_customer_data:
            cursor.execute(query, customer)

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