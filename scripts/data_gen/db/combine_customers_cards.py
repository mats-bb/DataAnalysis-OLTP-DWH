import os

os.sys.path.append('scripts')
from util.utils import load_from_json, save_to_json

DATA_GEN_PATH = r"data\data_gen"


customer_data = load_from_json(DATA_GEN_PATH, "customer_data.json")
customer_cards = load_from_json(DATA_GEN_PATH, "customer_cards.json")

transformed_customers = []

for idx, customer in enumerate(customer_data):
    customer["card_info"] = customer_cards[idx]
    customer["card_info"]["cardholder_name"] = customer["first_name"] + " " + customer["last_name"]
    transformed_customers.append(customer)

save_to_json(DATA_GEN_PATH, "combined_customer_data.json", transformed_customers)