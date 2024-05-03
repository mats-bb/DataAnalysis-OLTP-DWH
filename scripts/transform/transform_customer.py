import json

RAW_PATH = r"data\raw"
TRANSFORMED_PATH = r"data\transformed"

def load_from_json(dir_, filename):
    """Load json file from directory."""

    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    

def save_to_json(dir_, filename, data):
    """Save json file to directory."""

    with open(fr'{dir_}\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


customer_data = load_from_json(RAW_PATH, "customer_data")
customer_cards = load_from_json(RAW_PATH, "customer_cards")

transformed_customers = []

for idx, customer in enumerate(customer_data):
    customer["card_info"] = customer_cards[idx]
    customer["card_info"]["cardholder_name"] = customer["first_name"] + " " + customer["last_name"]
    transformed_customers.append(customer)

save_to_json(TRANSFORMED_PATH, "transformed_customers", transformed_customers)