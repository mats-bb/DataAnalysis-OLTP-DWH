import re
import os
import json

os.sys.path.append('scripts')
from util.utils import load_from_json, get_soup, save_to_json, get_resp

EXTRACTED_DIR = r"data\db\extracted"
URLS_FILE_NAME = "urls.json"
FILE_NAME = None


def get_product_description(soup):
    """Return product description."""

    # Find the correct div for the product data
    basic_product_data = json.loads(soup.find("script", type="application/ld+json").string)
    product_description = {"description": basic_product_data["description"]}
    
    return product_description


def get_product_spec_sheet(soup):
    """Return product spec sheet."""

    spec_list = []

    # Find the correct div for the product spec sheet data
    spec_tables = soup.find_all("table", class_="responsive-table fixed-layout")

    for table in spec_tables:
        table_dict = {}

        table_dict["caption"] = table.caption.text.lower()

        for row in table.tbody.find_all('tr'):
            table_dict[row.th.text.lower()] = row.td.text.lower()

        spec_list.append(table_dict)

    return spec_list


def get_product_information(soup):
    """Return dict containing all relevant product data."""

    # Find the correct div for the product data

    script_tag = soup.find('script', string=re.compile(r'productId'))

    script_content = script_tag.string

    # Get the dictionary values from the script tag
    data_match = re.search(r'dataLayer.push\((\{.*?\})\);', script_content, re.DOTALL)
    json_data = data_match.group(1)
    data_dict = json.loads(json_data)

    # Get description
    product_description = get_product_description(soup)
    # Get spec sheet
    product_spec_sheet = get_product_spec_sheet(soup)

    # Update the data dict with the product description and spec sheet
    data_dict.update(product_description)
    data_dict["product_spec_sheet"] = product_spec_sheet

    return data_dict


def extract_product_data():

    urls = load_from_json(EXTRACTED_DIR, URLS_FILE_NAME)
    
    extracted_product_data = []

    # Apply logic for each url and persist data to json
    for url in urls:
        resp = get_resp(url)
        if resp:

            soup = get_soup(resp)
            product_data = get_product_information(soup)
            extracted_product_data.append(product_data)

    save_to_json(EXTRACTED_DIR, FILE_NAME, extracted_product_data)

extract_product_data()