import json
import psycopg2
import dotenv
import os

dotenv.load_dotenv()

TRANSFORMED_DIR = fr"data\transformed"

connection_params = {
    "host": os.environ["DATABASE_IP"],
    "database": os.environ["DATABASE_NAME"],
    "port": os.environ["DATABASE_PORT"],
    "user": os.environ["DATABASE_USERNAME"],
    "password": os.environ["DATABASE_PASSWORD"]
}


def load_from_json(dir_, filename):
    """Load json file from directory."""

    with open(fr'{dir_}\{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    

def load_data(connection_params):
    """Load data into database."""

    customers = load_from_json(TRANSFORMED_DIR, "transformed_customers")

    try:
        conn = psycopg2.connect(**connection_params)
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
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

load_data(connection_params)