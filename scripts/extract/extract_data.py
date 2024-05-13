import json
import os

os.sys.path.append('scripts')
from util.utils import get_resp, get_soup, save_to_json, load_from_json


RAW_DIR = rf"data\raw"



def get_basic_data(soup):
    """Return basic product json."""

    basic_product_data = json.loads(soup.find("script", type="application/ld+json").string)
    
    return basic_product_data

def clean_basic_data(basic_product_data):
    """Return only select data from basic product json."""

    keys_to_keep = ["name", "description", "sku", "mpn"]

    clean_product_data = {}

    for key, val in basic_product_data.items():
        if key in keys_to_keep:
            clean_product_data[key] = val

    clean_product_data["producer"] = basic_product_data["brand"]["name"]

    # Product out of stock. Adjust DB and script accordingly
    try:
        clean_product_data["price"] = basic_product_data["offers"]["price"]
    except KeyError:
        clean_product_data["price"] = 0

    return clean_product_data


def get_product_categories(url):
    """Return product categories."""

    categories_list = url.split("/")[5:8]

    category_out_dict = {
        "main_category": categories_list[0],
        "type_category": categories_list[1],
        "product_category": categories_list[2]
    }

    return category_out_dict


def get_product_spec_sheet(soup):
    """Return product spec sheet."""

    spec_list = []

    spec_tables = soup.find_all("table", class_="responsive-table fixed-layout")

    for table in spec_tables:
        table_dict = {}

        table_dict["caption"] = table.caption.text.lower()

        for row in table.tbody.find_all('tr'):
            table_dict[row.th.text.lower()] = row.td.text.lower()

        spec_list.append(table_dict)

    return spec_list


def combine_product_data(clean_product_data, soup, url):
    """Combine the product data."""

    product_categories = get_product_categories(url)
    product_spec_sheet = get_product_spec_sheet(soup)

    combined_product_data = clean_product_data 

    combined_product_data["categories"] = product_categories
    combined_product_data["spec_sheet"] = product_spec_sheet

    return combined_product_data


def get_all_products(urls):
    """Combine all products. Return list of dicts."""

    all_products_info = []
    
    for url in urls:
        resp = get_resp(url)
        soup = get_soup(resp)
        basic_product_data = get_basic_data(soup)
        clean_product_data = clean_basic_data(basic_product_data)
        combined_product_data = combine_product_data(clean_product_data, soup, url)
        all_products_info.append(combined_product_data)

    return all_products_info


def run():
    urls = load_from_json(RAW_DIR, "urls")
    all_products_info = get_all_products(urls)

    save_to_json(RAW_DIR, "combined_product_data", all_products_info)

run()


# def get_product_imgs():
#     """Return product images."""
#     pass

# def get_product_info_sheet():
#     """Return product info sheet."""
#     pass
