import json
import psycopg2


RAW_DIR = fr"data\raw"

connection_params = {
    "host": "localhost",
    "database": "komplett",
    "user": "postgres",
    "password": "*"
}

def load_from_json(dir_, filename):
    """Load json file from directory."""

    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_data(connection_params):
    """Load data into database."""

    products = load_from_json(RAW_DIR, "combined_product_data")

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        for product in products:
            d = {
                "main_category_name": product["categories"]["main_category"],
                "type_category_name": product["categories"]["type_category"],
                "product_category_name": product["categories"]["product_category"],
                "producer_name": product["producer"],
                "product_name": product["name"],
                "product_description": product["description"],
                "price": product["price"], 
                "specs": json.dumps(product["spec_sheet"]),
                "sku": product["sku"],
                "mpn": product["mpn"],
                "quantity": 0
            }

            # Call the stored procedure with unpacked values
            cursor.execute("CALL insert_product_data(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", [d[key] for key in d.keys()])

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