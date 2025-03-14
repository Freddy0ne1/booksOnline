import requests 
from bs4 import BeautifulSoup
import csv

# URL du livre
url = "https://books.toscrape.com/catalogue/emma_17/index.html"

# Lancer la requête HTTP
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")

# Ajout de l'URL du produit
product_page_url_text = [url]

# Extraction category, title
page = soup.find("div", class_="container-fluid page")
categories = page.find("ul").find_all("li")[2].get_text(strip=True)
category_text = [categories]

titles = page.find("ul").find_all("li")[3]
title_text = []
for title in titles:
    title_text.append(title.string)
    
# Extraction product_description
product_descriptions = soup.find_all("p")[3]
product_description_text = []
for product_description in product_descriptions:
    product_description_text.append(product_description.string)

# Extraction upc prices number_available review_rating
table = soup.find("table", class_="table table-striped")
upc = table.find_all("td")[0]
universal_product_code_text = []
for universal_product_code in upc:
    universal_product_code_text.append(universal_product_code.string)

i_taxes = table.find_all("td")[3]
price_including_tax_text = []
for price_including_tax in i_taxes:
    price_including_tax_text.append(price_including_tax.string)

e_taxes = table.find_all("td")[2]
price_excluding_tax_text = []
for price_excluding_tax in e_taxes:
    price_excluding_tax_text.append(price_excluding_tax.string)

num_availables = table.find_all("td")[5]
number_available_text = []
for number_available in num_availables:
    number_available_text.append(number_available.string)

r_ratings = table.find_all("td")[6]
review_rating_text = []
for review_rating in r_ratings:
    review_rating_text.append(review_rating.string)

# Extraction image
image = soup.find("div", class_="item active")
image_url_text = []

if image:
    image_tag = image.find("img")
    if image_tag and "src" in image_tag.attrs:
        image_url = image_tag["src"]  # On récupère directement l'URL
        image_url_text.append(image_url)

# Ecrire dans le fichier CSV
en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
with open("../data.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(en_tete)
    for product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_url_text, universal_product_code_text, title_text, price_including_tax_text, price_excluding_tax_text, number_available_text, product_description_text, category_text, review_rating_text, image_url_text):
        writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])