import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import load_from_json, connect_db

TRANSFORMED_DIR = fr"data\transformed"

def load_order_rows():

    order_rows = load_from_json(TRANSFORMED_DIR, "transformed_order_rows")

    try:
        conn = connect_db('komplett_dwh')
        cursor = conn.cursor()

        for row in order_rows:
            row = json.dumps(row)

            cursor.execute("CALL insert_order_data(%s);", (row,))

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

load_order_rows()