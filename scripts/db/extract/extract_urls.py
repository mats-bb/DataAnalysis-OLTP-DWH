# To make things simple, lets choose a product category, for example graphics cards
# Fetch URL for all graphics cards
# Fetch URLs for all graphics cards
# Fetch data from each URL
# Store data (JSON?)

# Things of notice in dev tools 
# "nlevel", "div class="search-show-more", "hits"
# product-link image-container


# Skjermkort
# "https://www.komplett.no/category/10412/datautstyr/pc-komponenter/skjermkort?nlevel=10000%C2%A728003%C2%A710412&hits=288"

# Prosessorer
# "https://www.komplett.no/category/11204/datautstyr/pc-komponenter/prosessorer?nlevel=10000%C2%A728003%C2%A711204&hits=120"

# RAM
# "https://www.komplett.no/category/11209/datautstyr/pc-komponenter/minnebrikker?nlevel=10000%C2%A728003%C2%A711209&hits=216"

# Hovedkort
# "https://www.komplett.no/category/10111/datautstyr/pc-komponenter/hovedkort?nlevel=10000%C2%A728003%C2%A710111&hits=144"


# NB!!! Will extract tilbehør urls as well. Needs fixing.

import os

os.sys.path.append('scripts')
from util.utils import get_resp, get_soup, save_to_json

BASE_URL = rf"https://www.komplett.no/category/11204/datautstyr/pc-komponenter/prosessorer?nlevel=10000%C2%A728003%C2%A711204&hits=120"

RAW_DIR = rf"data\raw"


def get_classes(soup, class_name):
    """Returns a list of classes from soup object."""
    classes = soup.find_all(class_=class_name)

    return classes


def get_urls(base_url):

    urls = []

    resp = get_resp(base_url)

    if resp.status_code == 200:
        soup = get_soup(resp)

        classes = get_classes(soup, "product-link image-container")

        for class_ in classes:
            urls.append(f"https://www.komplett.no{class_['href']}")

    return urls

def extract_urls():
    urls = get_urls(BASE_URL)
    save_to_json(RAW_DIR, 'urls', urls)

extract_urls()

# resp = get_resp(BASE_URL, headers)

# print(resp.content)