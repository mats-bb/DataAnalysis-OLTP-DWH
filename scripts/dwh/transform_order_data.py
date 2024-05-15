import os

os.sys.path.append('scripts')
from util.utils import load_from_json, save_to_json

EXTRACTED_DIR = fr"data\extracted"
TRANSFORMED_DIR = fr"data\transformed"


def calculate_discounted_price(row):
    regular_unit_price = row['regular_unit_price']
    discount_amount = row['discount_amount']
    discount_type = row.get('discount_type')

    if discount_type == 'Percentage':
        return regular_unit_price - regular_unit_price * (discount_amount / 100)
    elif discount_type == 'Dollar Amount':
        return regular_unit_price - discount_amount
    

def calculate_net_price(row):
    regular_unit_price = row['regular_unit_price']
    discounted_unit_price = row.get('discounted_price')

    if discounted_unit_price:
        return discounted_unit_price + row['delivery_price']
    else:
        return regular_unit_price + row['delivery_price']
    

def calculate_extended_sales_amount(row):
    return row['net_price'] * row['quantity']


def calculate_extended_discount_amount(row):

    if row.get('discounted_price'):
        return row['discounted_price'] * row['quantity']
    return None


def convert_discount_id(row):

    if not row.get('discount_id'):
        return 0
    return int(row['discount_id'])


def remove_keys(row):

    row.pop('discount_type')
    row.pop('discount_amount')
    row.pop('delivery_price')


def transform_order_rows():

    transformed_order_rows = []
    rows = load_from_json(EXTRACTED_DIR, "extracted_orders")

    for row in rows:
        # row = {key: value for key, value in row.items()}
        row['discounted_price'] = calculate_discounted_price(row)
        row['net_price'] = calculate_net_price(row)
        row['extended_sales_amount'] = calculate_extended_sales_amount(row)
        row['extended_discount_amount'] = calculate_extended_discount_amount(row)
        row['discount_id'] = convert_discount_id(row)
        remove_keys(row)
        transformed_order_rows.append(row)

    save_to_json(TRANSFORMED_DIR, "transformed_order_rows", transformed_order_rows)

transform_order_rows()