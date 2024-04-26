# Classes to look up for item data

# Name: "product-main-info-webtext1"
# Description: "product-main-info-webtext2"
# Producer name: "product-main-info-manufacturerName"
# Category
    # Main
    # Type
    # Product
# Price: "product-price" priceNowRaw
# Imgs: ""
# Info: ""
# Specs: ""
# Inventory
    # SKU: ""
    # Quantity: ""


import requests as req
from bs4 import BeautifulSoup as bs
import json
import pandas as pd

URL = "https://www.komplett.no/product/1249267/datautstyr/pc-komponenter/skjermkort/asus-proart-geforce-rtx-4060-ti-oc"

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


def get_classes(soup, class_name):
    """Returns a list of classes from soup object."""
    classes = soup.find_all("table", class_="responsive-table fixed-layout")

    return classes

resp = get_resp(URL, headers)
soup = get_soup(resp)

# Name: "product-main-info-webtext1"
name = soup.find(class_="product-main-info-webtext1")
print(name.find("span").text)

# Description: "product-main-info-webtext2"
description = soup.find(class_="product-main-info-webtext2")
print(description.find("span").text)

# Producer name: "product-main-info-manufacturerName"
prod_name = soup.find(class_="product-main-info-manufacturerName")
print(prod_name.find("a").text.strip())

# Category
    # Main
    # Type
    # Product





# Price: "product-price" priceNowRaw
# Imgs: ""
# Info: ""
# Specs: ""
# Inventory
    # SKU: ""
    # Quantity: ""







# Get specs
l = []

tables = soup.find_all("table")

for table in tables:
    d = {}
    d["caption"] = table.caption.text.lower()
    for row in table.tbody.find_all('tr'):    
        d[row.th.text.lower()] = row.td.text.lower()
    
    l.append(d)

# print(l)
# End specs

def get_name():
    pass

def get_description():
    pass

def get_producer_name():
    pass

def get_category():
    pass

def get_price():
    pass

def get_imgs():
    pass

def get_info():
    pass

def get_specs():
    pass

def get_inventory():
    pass

