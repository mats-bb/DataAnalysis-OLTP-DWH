import json
import psycopg2
import os

os.sys.path.append('scripts')
from util.utils import load_from_json, connect_db


TRANSFORMED_DIR = fr"data\transformed"
 

def load_data():
    """Load data into database."""

    customers = load_from_json(TRANSFORMED_DIR, "transformed_customers")

    try:
        conn = connect_db()
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

load_data()





# def load_data(connection_params):
#     """Load data into database."""

#     customers = load_from_json(TRANSFORMED_DIR, "transformed_customers")

#     try:
#         conn = psycopg2.connect(**connection_params)
#         cursor = conn.cursor()

#         for customer in customers:
#             customer = json.dumps(customer)

#             # Call the stored procedure with unpacked values
#             cursor.execute("CALL insert_customer_data(%s);", (customer,))

#         # Commit the transaction
#         conn.commit()
#         print("Data inserted successfully!")

#     except psycopg2.Error as e:
#         conn.rollback()
#         print("Error:", e)

#     finally:
#         # Close the cursor and connection
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()