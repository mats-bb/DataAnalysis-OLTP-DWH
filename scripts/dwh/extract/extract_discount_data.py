import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = "extracted_discount_data.json"

def extract_location_data():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT id, discount_name, discount_type, amount, start_date::text, end_date::text
            FROM discount;
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


extract_location_data()