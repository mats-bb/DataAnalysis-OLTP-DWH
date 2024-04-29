import requests as req
from bs4 import BeautifulSoup as bs
import json
import pandas as pd

URL = "https://www.komplett.no/product/1303149/datautstyr/pc-komponenter/skjermkort/asus-dual-geforce-rtx-4070-super-oc-hvit"

RAW_DIR = rf"data\raw"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def get_resp(url, headers):
    """Get response from url."""
    return req.get(url, headers=headers)


def get_soup(resp):
    """Get soup object from response."""
    return bs(resp.content, "html.parser")


def save_to_json(dir_, filename, data):
    """Save json file to directory."""
    with open(fr'{dir_}/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_from_json(dir_, filename):
    """Load json file from directory."""
    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)


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
    try:
        clean_product_data["price"] = basic_product_data["offers"]["price"]
    except KeyError:
        clean_product_data["price"] = 0

    return clean_product_data

def get_product_categories(soup):
    """Return product categories."""
    category_data = soup.find("script", id="breadcrumbsScript")
    category_data_str = category_data.get("data-model")
    category_data_dict = json.loads(category_data_str)
    category_data_list = category_data_dict["breadCrumb"].split("|")[1:]
    category_out_dict = {
        "main_category": category_data_list[0],
        "type_category": category_data_list[1],
        "product_category": category_data_list[2]
    }

    return category_out_dict


def get_product_spec_sheet(soup):
    """Return product spec sheet."""

    spec_list = []

    spec_tables = soup.find_all("table", class_="responsive-table fixed-layout")

    for table in spec_tables:
        table_dict = {}

        try:
            table_dict["caption"] = table.caption.text.lower()
        except AttributeError:
            print(json.loads(soup.find("script", type="application/ld+json").string)["name"])

        for row in table.tbody.find_all('tr'):
            table_dict[row.th.text.lower()] = row.td.text.lower()

        spec_list.append(table_dict)

    return spec_list


def combine_product_data(clean_product_data, soup):
    product_categories = get_product_categories(soup)
    product_spec_sheet = get_product_spec_sheet(soup)

    combined_product_data = clean_product_data 

    combined_product_data["categories"] = product_categories
    combined_product_data["spec_sheet"] = product_spec_sheet

    return combined_product_data

def get_all_products(urls):

    all_products_info = []
    
    for url in urls:
        resp = get_resp(url, headers)
        soup = get_soup(resp)
        basic_product_data = get_basic_data(soup)
        clean_product_data = clean_basic_data(basic_product_data)
        combined_product_data = combine_product_data(clean_product_data, soup)
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
