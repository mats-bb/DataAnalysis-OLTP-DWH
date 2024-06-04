import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = r"extracted_location_data.json"

def extract_location_data():

    try:
        conn = connect_db('komplett_v2_oltp')
        cursor = conn.cursor()

        query = """
            SELECT a.id, a.street_address, a.zip_code, c.city_name, s.state_name 
            FROM address a
            JOIN city c ON a.city_id = c.id 
            JOIN state s ON c.state_id = s.id;
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