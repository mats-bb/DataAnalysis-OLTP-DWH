import os

os.sys.path.append('scripts')
from util.utils import get_resp, get_soup, save_to_json

# Extract URLs for given products from komplett.no
# Some manual work went into this, as shown below. As some products have different page content, this was necessary
# for testing purposes, and eventually a one-time operation.

# CPUs
# BASE_URL = r"https://www.komplett.no/category/11204/datautstyr/pc-komponenter/prosessorer?nlevel=10000%C2%A728003%C2%A711204&hits=120"

# Casemods
# BASE_URL = r"https://www.komplett.no/category/10021/datautstyr/pc-komponenter/casemods"

# Kabinetter
# BASE_URL = r"https://www.komplett.no/category/10149/datautstyr/pc-komponenter/kabinetter/barebone?nlevel=10000%C2%A728003%C2%A710149&hits=168"

# Kontrollere
# BASE_URL = r"https://www.komplett.no/category/10204/datautstyr/pc-komponenter/kontrollere"

# Lydkort
# BASE_URL = r"https://www.komplett.no/category/11211/datautstyr/pc-komponenter/lydkort"

# RAM
# BASE_URL = r"https://komplett.no/category/11209/datautstyr/pc-komponenter/minnebrikker?nlevel=10000%C2%A728003%C2%A711209&hits=216"

# Skjermkort
# BASE_URL = r"https://www.komplett.no/category/10412/datautstyr/pc-komponenter/skjermkort?nlevel=10000%C2%A728003%C2%A710412&hits=240"

# PSU
# BASE_URL = r"https://www.komplett.no/category/10057/datautstyr/pc-komponenter/stroemforsyning?nlevel=10000%C2%A728003%C2%A710057&hits=96"

# Vifter
# BASE_URL = r"https://www.komplett.no/category/10462/datautstyr/pc-komponenter/vifter/kjoeling/vannkjoeling?nlevel=10000%C2%A728003%C2%A710462&hits=336"

# Hovedkort
# BASE_URL = r"https://www.komplett.no/category/10111/datautstyr/pc-komponenter/hovedkort?nlevel=10000%C2%A728003%C2%A710111&hits=144"

# Lagring
BASE_URL = r"https://www.komplett.no/category/10088/datautstyr/lagring/harddisker/ssd?nlevel=10000%C2%A728001%C2%A710088&hits=264"

EXTRACTED_DIR = r"data\db\extracted"
FILE_NAME = "urls.json"


def get_divs(soup, class_name):
    """Returns a list of divs from soup object."""
    classes = soup.find_all(class_=class_name)

    return classes


def get_urls(base_url):
    """Extract urls from base URL."""

    urls = []

    resp = get_resp(base_url)
    print(resp.status_code)

    # Get beautiful soup object from response
    if resp.status_code == 200:
        soup = get_soup(resp)

        # Get list of product links from soup object
        classes = get_divs(soup, "product-link image-container")

        for class_ in classes:
            urls.append(f"https://www.komplett.no{class_['href']}")
    

    return urls


def extract_urls():
    """Run extraction."""
    
    urls = get_urls(BASE_URL)
    save_to_json(EXTRACTED_DIR, FILE_NAME, urls)

extract_urls()