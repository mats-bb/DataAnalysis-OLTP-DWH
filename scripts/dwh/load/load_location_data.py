import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

EXTRACTED_DIR = r"data\dwh\extracted"
FILE_NAME = "extracted_location_data.json"

def load_location_data():
    """Load data into database."""

    extracted_location_data = load_from_json(EXTRACTED_DIR, FILE_NAME)

    try:
        conn = connect_db('komplett_v2_dwh')
        cursor = conn.cursor()

        query = """INSERT INTO Dim_location (id, street_address, zip_code, city_name, state_name)
                    VALUES (%s, %s, %s, %s, %s)"""

        for location in extracted_location_data:
            cursor.execute(query, location)

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

load_location_data()