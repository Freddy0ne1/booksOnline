import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin
from tqdm import tqdm
import re

# URL de base du site à scraper (ATTENTION : le site est uniquement accessible en HTTP)
BASE_SITE_URL = "http://books.toscrape.com/"

# Fonction pour récupérer toutes les catégories disponibles sur le site
def get_all_categories():
    response = requests.get(BASE_SITE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    category_elements = soup.select("div.side_categories ul li ul li a")

    categories = {}
    for cat in category_elements:
        name = cat.text.strip()  # Nom de la catégorie
        href = cat["href"]  # Lien relatif
        url = urljoin(BASE_SITE_URL, href)  # URL absolue
        categories[name] = url

    return categories

# Fonction pour récupérer tous les liens de livres d'une page donnée
def get_books_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for article in soup.select(".product_pod"):
        # Construction de l'URL absolue du livre
        book_url = urljoin(BASE_SITE_URL, "catalogue/" + article.h3.a["href"].replace("../../../", ""))
        books.append(book_url)

    # Vérifie s'il y a une page suivante
    next_page = soup.select_one(".next a")
    next_url = url.rsplit('/', 1)[0] + "/" + next_page["href"] if next_page else None

    return books, next_url

# Fonction pour extraire les données d'un livre à partir de sa page produit
def scrape_product(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8" # Forçage d'encodage utf-8
    soup = BeautifulSoup(response.text, "html.parser")

    product_page_url = url
    upc = soup.find("th", string="UPC").find_next("td").text
    title = soup.find("h1").text
    price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text

    # Récupère le nombre d'exemplaires disponibles
    number_available = re.search(r"\d+", soup.find("th", string="Availability").find_next("td").text)
    number_available = number_available.group() if number_available else "0"

    # Récupère la description si elle existe
    description_tag = soup.find("meta", {"name": "description"})
    product_description = description_tag["content"].strip() if description_tag else ""

    # Catégorie du livre
    category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].text.strip()

    # Note du livre (ex : One, Two, Three, Four, Five)
    review_rating = soup.find("p", class_="star-rating")["class"][1]

    # URL de l'image du livre
    image_url = soup.find("img")["src"].replace("../../", "")
    image_url = urljoin(BASE_SITE_URL, image_url)

    return {
        "product_page_url": product_page_url,
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

# Fonction pour télécharger l'image d'un livre
def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url} : {e}")

# Fonction pour scraper tous les livres d'une catégorie
def scrape_books_from_category(category_name, category_url, output_folder):
    print(f"\nScraping catégorie : {category_name}")
    url = category_url
    book_urls = []

    # Parcours des pages de la catégorie
    while url:
        print(f"  Page: {url}")
        books, url = get_books_from_page(url)
        book_urls.extend(books)

    books_data = []
    safe_category = category_name.lower().replace(" ", "_")
    image_folder = os.path.join(output_folder, "images", safe_category)
    os.makedirs(image_folder, exist_ok=True)

    # Scraping de chaque livre de la catégorie
    for book_url in tqdm(book_urls, desc=f"  → Livres {category_name}"):
        try:
            book_data = scrape_product(book_url)
            books_data.append(book_data)

            # Nettoyage du nom du fichier image
            image_filename = re.sub(r'[\\/*?:"<>|]', "_", book_data["title"])[:100] + ".jpg"
            image_path = os.path.join(image_folder, image_filename)
            download_image(book_data["image_url"], image_path)
        except Exception as e:
            print(f"Erreur lors du scraping de {book_url} : {e}")

    return books_data

# Fonction pour sauvegarder les données dans un fichier CSV
def save_to_csv(books, category_name, output_folder):
    if not books:
        return

    safe_category_name = category_name.lower().replace(" ", "_")
    filename = f"books_{safe_category_name}.csv"
    filepath = os.path.join(output_folder, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    print(f"Données sauvegardées dans : {filepath}")

if __name__ == "__main__":
     # Demande à l'utilisateur s'il souhaite démarrer le scraping
    start = input("Voulez-vous démarrer le scraping ? (o/n) : ").strip().lower()
    if start != "o":
        print("Scraping annulé.")
        exit()

    # Demande à l'utilisateur le dossier de sortie
    chemin_dossier = input("Où voulez-vous créer le dossier de sortie ? (ex: C:/Users/VotreNom/Documents ou ./ pour le dossier courant) : ").strip()
    nom_dossier = input("Quel nom voulez-vous donner au dossier de sortie ? : ").strip()
    
    chemin_complet = os.path.join(chemin_dossier, nom_dossier)

    if not os.path.exists(chemin_complet):
        os.makedirs(chemin_complet)
        print(f"Dossier '{chemin_complet}' créé avec succès.")
    else:
        print(f"Le dossier '{chemin_complet}' existe déjà.")

    # Récupère toutes les catégories
    categories = get_all_categories()

    # Scrape chaque catégorie et sauvegarde les données
    for category_name, category_url in categories.items():
        books_data = scrape_books_from_category(category_name, category_url, chemin_complet)
        save_to_csv(books_data, category_name, chemin_complet)

    print("\nScraping terminé pour toutes les catégories.")
