import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from tqdm import tqdm
import os
from config import BASE_SITE_URL
from image_downloader import download_image
from utils import clean_filename

def get_books_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for article in soup.select(".product_pod"):
        book_url = urljoin(BASE_SITE_URL, "catalogue/" + article.h3.a["href"].replace("../../../", ""))
        books.append(book_url)

    next_page = soup.select_one(".next a")
    next_url = url.rsplit('/', 1)[0] + "/" + next_page["href"] if next_page else None

    return books, next_url

def scrape_product(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    upc = soup.find("th", string="UPC").find_next("td").text
    title = soup.find("h1").text
    price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    availability = soup.find("th", string="Availability").find_next("td").text
    number_available = re.search(r"\d+", availability)
    number_available = number_available.group() if number_available else "0"
    description_tag = soup.find("meta", {"name": "description"})
    product_description = description_tag["content"].strip() if description_tag else ""
    category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].text.strip()
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = soup.find("img")["src"].replace("../../", "")
    image_url = urljoin(BASE_SITE_URL, image_url)

    return {
        "product_page_url": url,
        "universal_product_code (upc)": upc,
        "title": title,
        "price_including_tax": price_incl_tax,
        "price_excluding_tax": price_excl_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }

def scrape_books_from_category(category_name, category_url, output_folder):
    print(f"\nScraping catégorie : {category_name}")
    url = category_url
    book_urls = []

    while url:
        print(f"  Page: {url}")
        books, url = get_books_from_page(url)
        book_urls.extend(books)

    books_data = []
    safe_category = category_name.lower().replace(" ", "_")
    image_folder = os.path.join(output_folder, "images", safe_category)
    os.makedirs(image_folder, exist_ok=True)

    for book_url in tqdm(book_urls, desc=f"  → Livres {category_name}"):
        try:
            book_data = scrape_product(book_url)
            books_data.append(book_data)
            image_filename = clean_filename(book_data["title"])[:100] + ".jpg"
            image_path = os.path.join(image_folder, image_filename)
            download_image(book_data["image_url"], image_path)
        except Exception as e:
            print(f"Erreur lors du scraping de {book_url} : {e}")

    return books_data
