import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import load_from_json, connect_db


DATA_GEN_DIR = fr"data\data_gen"
FILE_NAME = "combined_customer_data.json"
 

def load_customer_data():
    """Load customer data into database."""

    customers = load_from_json(DATA_GEN_DIR, FILE_NAME)

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        for customer in customers:
            customer = json.dumps(customer)

            # Call the stored procedure with unpacked values
            cursor.execute("CALL insert_customer_data(%s);", (customer,))

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

load_customer_data()