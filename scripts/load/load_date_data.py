import os
import json
import psycopg2

os.sys.path.append('scripts')
from util.utils import connect_db, load_from_json

RAW_DIR = rf'data\raw'


def load_data():
    """Load data into database."""

    dates = load_from_json(RAW_DIR, "date_data")

    try:
        conn = connect_db('komplett_dwh')
        cursor = conn.cursor()

        for date in dates:
            # date = json.dumps(date)

            # Call the stored procedure with unpacked values
            cursor.execute("""INSERT INTO dim_date(date, day_of_week, day_of_month, day_of_year,
                           week_number, year, name_of_day, name_of_month, month_number, quarter_number,
                           full_date_description, month_end_flag, weekday_flag, holiday_flag)
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", [date[key] for key in date.keys()])

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