import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import load_from_json, connect_db

RAW_PATH = r"data\raw"


def get_locations():

    customers = load_from_json(RAW_PATH, "customer_data")

    locations = []

    for customer in customers:
        
        location = {
            "zip_code": customer["zip"],
            "city_name": customer["city"],
            "state_name": customer["state"]
        }

        locations.append(location)

    return locations

def load_locations():

    locations = get_locations()

    try:
        conn = connect_db('komplett_dwh')
        cursor = conn.cursor()

        for location in locations:

            cursor.execute("""INSERT INTO dim_location (zip_code, city_name, state_name)
                           VALUES (%s, %s, %s)""", [location[key] for key in location.keys()])

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

load_locations()