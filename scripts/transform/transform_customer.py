import os

os.sys.path.append('scripts')
from util.utils import load_from_json, save_to_json

RAW_PATH = r"data\raw"
TRANSFORMED_PATH = r"data\transformed"


customer_data = load_from_json(RAW_PATH, "customer_data")
customer_cards = load_from_json(RAW_PATH, "customer_cards")

transformed_customers = []

for idx, customer in enumerate(customer_data):
    customer["card_info"] = customer_cards[idx]
    customer["card_info"]["cardholder_name"] = customer["first_name"] + " " + customer["last_name"]
    transformed_customers.append(customer)

save_to_json(TRANSFORMED_PATH, "transformed_customers", transformed_customers)