# To make things simple, lets choose a product category, for example graphics cards
# Fetch URL for all graphics cards
# Fetch URLs for all graphics cards
# Fetch data from each URL
# Store data (JSON?)

# Things of notice in dev tools 
# "nlevel", "div class="search-show-more", "hits"
# product-link image-container


# Full URL for now. Will figure out how to dynamically get complete URLs
# https://www.komplett.no/category/10412/datautstyr/pc-komponenter/skjermkort?nlevel=10000%C2%A728003%C2%A710412&hits=288


import requests as req
from bs4 import BeautifulSoup as bs
import json

BASE_URL = rf"https://www.komplett.no/category/10412/datautstyr/pc-komponenter/skjermkort?nlevel=10000%C2%A728003%C2%A710412&hits=288"

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


def get_classes(soup, class_name):
    """Returns a list of classes from soup object."""
    classes = soup.find_all(class_=class_name)

    return classes


def get_urls(base_url):

    urls = []

    resp = get_resp(base_url, headers)

    if resp.status_code == 200:
        soup = get_soup(resp)

        classes = get_classes(soup, "product-link image-container")

        for class_ in classes:
            urls.append(f"https://www.komplett.no{class_['href']}")

    return urls

def run():
    urls = get_urls(BASE_URL)
    save_to_json(RAW_DIR, 'urls', urls)

run()

# resp = get_resp(BASE_URL, headers)

# print(resp.content)