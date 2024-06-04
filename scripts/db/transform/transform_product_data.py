import os

os.sys.path.append('scripts')
from util.utils import load_from_json, save_to_json

EXTRACTED_DIR = r"data\backup"
TRANSFORMED_DIR = r"data\db\transformed"


def get_extraced_files(_dir):
    """Returns a list of file names from directory."""

    return os.listdir(_dir)

def transform_product_data():
    """Transform product data into desired format."""

    extracted_product_paths = get_extraced_files(EXTRACTED_DIR)

    for product_file_name in extracted_product_paths:
        extracted_product_data = load_from_json(EXTRACTED_DIR, product_file_name)

        transformed_product_list = []

        # Build product dictionary from product data and persist to json
        for data in extracted_product_data:
            # Check if ecommerce key exists, if not pass, else continue
            if not data.get("ecommerce"):
                pass
            else:

                transformed_product_dict = {
                    "name": data["ecommerce"]["items"][0]["item_name"],
                    "description": data["description"],
                    "sku": data["productId"],
                    "mpn": data["ecommerce"]["items"][0]["item_manufacturer_number"],
                    "producer": data["ecommerce"]["items"][0]["item_brand"],
                    "price": round(data["ecomm_shelfPrice"]),
                    "categories": {
                        "main_category": data["ecommerce"]["items"][0]["item_category"],
                        "type_category": data["ecommerce"]["items"][0]["item_category2"]
                    },
                    "spec_sheet": data["product_spec_sheet"]
                }

                # Check if fourth item category
                try:
                    item_category4 = data["ecommerce"]["items"][0]["item_category4"]
                except KeyError:
                    pass

                # If fourth category and == "Tilbehør", item_category3 = "Tilbehør
                if item_category4:
                    if item_category4 == "Tilbehør":
                        transformed_product_dict["categories"]["product_category"] = item_category4
                    else:
                        transformed_product_dict["categories"]["product_category"] = data["ecommerce"]["items"][0]["item_category3"]

                transformed_product_list.append(transformed_product_dict)

        transformed_file_name = product_file_name.replace('extracted', 'transformed')
        save_to_json(TRANSFORMED_DIR, transformed_file_name, transformed_product_list)

transform_product_data()