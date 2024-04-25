import requests as req
from bs4 import BeautifulSoup as bs
import json

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
    classes = soup.find_all(class_=class_name)

    return classes

resp = get_resp(URL, headers)
soup = get_soup(resp)
classes = get_classes(soup, "responsive-table fixed-layout")

l = []

for i in classes:
    for j in i:
        l.append(j.text)

print(l)