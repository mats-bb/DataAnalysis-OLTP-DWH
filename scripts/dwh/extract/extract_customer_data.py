import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"

def extract_customer_data():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT id, first_name, last_name,
                CASE 
                    WHEN middle_name IS NULL
                    THEN CONCAT(first_name, ' ', last_name)
                    ELSE CONCAT(first_name, ' ', middle_name, ' ', last_name)
                END AS full_name,
                dob::text, email, mobile_num, created_date::text
            FROM customer;
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


    save_to_json(EXTRACTED_DIR, "extracted_customer_data.json", rows)


extract_customer_data()