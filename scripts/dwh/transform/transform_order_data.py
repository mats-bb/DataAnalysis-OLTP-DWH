import os

os.sys.path.append('scripts')
from util.utils import load_from_json, save_to_json

EXTRACTED_DIR = r"data\dwh\extracted"
TRANSFORMED_DIR = r"data\dwh\transformed"
EXTRACTED_FILE_NAME = "extracted_order_data.json"
TRANSFORMED_FILE_NAME = "transformed_order_data.json"

def calculate_discounted_price(row):
    regular_unit_price = row['regular_unit_price']
    discount_amount = row['discount_amount']
    discount_type = row.get('discount_type')

    if discount_type == 'Percentage':
        return round(regular_unit_price - regular_unit_price * (discount_amount / 100))
    elif discount_type == 'Dollar Amount':
        return round(regular_unit_price - discount_amount)
    

def calculate_net_price(row):
    regular_unit_price = row['regular_unit_price']
    discounted_unit_price = row.get('discounted_price')

    if discounted_unit_price:
        return discounted_unit_price + row['delivery_price']
    else:
        return regular_unit_price + row['delivery_price']
    

def calculate_extended_sales_amount(row):

    return int(row['net_price'] * row['quantity'])


def calculate_extended_discount_amount(row):

    if row.get('discounted_price'):
        return int(row['discounted_price'] * row['quantity'])
    return None


def remove_keys(row):

    row.pop('discount_type')
    row.pop('discount_amount')
    row.pop('delivery_price')
    row.pop('product_name')


def transform_order_rows():

    transformed_order_rows = []
    rows = load_from_json(EXTRACTED_DIR, EXTRACTED_FILE_NAME)

    for row in rows:
        row['discounted_price'] = calculate_discounted_price(row)
        row['net_price'] = calculate_net_price(row)
        row['extended_sales_amount'] = calculate_extended_sales_amount(row)
        row['extended_discount_amount'] = calculate_extended_discount_amount(row)
        remove_keys(row)
        transformed_order_rows.append(row)

    save_to_json(TRANSFORMED_DIR, TRANSFORMED_FILE_NAME, transformed_order_rows)

transform_order_rows()