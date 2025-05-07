import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import BASE_SITE_URL

def get_all_categories():
    response = requests.get(BASE_SITE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    category_elements = soup.select("div.side_categories ul li ul li a")

    categories = {}
    for cat in category_elements:
        name = cat.text.strip()
        href = cat["href"]
        url = urljoin(BASE_SITE_URL, href)
        categories[name] = url

    return categories
