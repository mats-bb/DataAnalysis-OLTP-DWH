import os
import dotenv
from bs4 import BeautifulSoup as bs
import json
import requests as req
import psycopg2

def connect_db(db_name):
    
    res = dotenv.load_dotenv()
    if not res:
        raise Exception("Could not load .env file")
    
    connection_params = {
        "host": os.environ["DATABASE_IP"],
        "database": db_name,
        "port": os.environ["DATABASE_PORT"],
        "user": os.environ["DATABASE_USERNAME"],
        "password": os.environ["DATABASE_PASSWORD"]
    }

    conn = psycopg2.connect(**connection_params)
    
    return conn


def load_from_json(dir_, filename):
    """Load json file from directory."""

    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_resp(url):
    """Get response from url."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    return req.get(url, headers=headers)


def get_soup(resp):
    """Get soup object from response."""
    return bs(resp.content, "html.parser")


def save_to_json(dir_, filename, data):
    """Save json file to directory."""
    with open(fr'{dir_}/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)