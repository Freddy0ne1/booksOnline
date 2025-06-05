# Import des modules nécessaires
import requests  # Pour effectuer les requêtes HTTP
from bs4 import BeautifulSoup  # Pour parser le HTML
from urllib.parse import urljoin  # Pour combiner des URLs
import re  # Pour les expressions régulières (extraire des chiffres notamment)
from tqdm import tqdm  # Pour afficher une barre de progression
import os  # Pour gérer les fichiers et répertoires

# Import des constantes et fonctions personnalisées
from config import BASE_SITE_URL  # URL de base du site
from image_downloader import download_image  # Fonction personnalisée pour télécharger une image
from utils import clean_filename  # Nettoie un nom de fichier (supprime les caractères invalides)

def get_books_from_page(url):
    # Envoie une requête HTTP à la page de catégorie
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    # Sélectionne tous les blocs de livre (chaque livre est dans un .product_pod)
    for article in soup.select(".product_pod"):
        # Construit l'URL complète du livre en nettoyant le chemin relatif
        book_url = urljoin(BASE_SITE_URL, "catalogue/" + article.h3.a["href"].replace("../../../", ""))
        books.append(book_url)

    # Vérifie s’il y a une page suivante
    next_page = soup.select_one(".next a")
    next_url = url.rsplit('/', 1)[0] + "/" + next_page["href"] if next_page else None

    return books, next_url  # Renvoie la liste des URLs de livres + URL de la prochaine page (ou None)

def scrape_product(url):
    # Envoie une requête HTTP au produit (page du livre)
    response = requests.get(url)
    response.raise_for_status()  # Lève une erreur si la requête échoue
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraction des données spécifiques du livre
    upc = soup.find("th", string="UPC").find_next("td").text
    title = soup.find("h1").text
    price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    availability = soup.find("th", string="Availability").find_next("td").text
    number_available = re.search(r"\d+", availability)  # Extrait le nombre disponible
    number_available = number_available.group() if number_available else "0"

    # Description du produit
    description_tag = soup.find("meta", {"name": "description"})
    product_description = description_tag["content"].strip() if description_tag else ""

    # Catégorie du livre
    category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].text.strip()

    # Évaluation (nombre d’étoiles)
    review_rating = soup.find("p", class_="star-rating")["class"][1]

    # URL de l’image du livre (reconstruite depuis le chemin relatif)
    image_url = soup.find("img")["src"].replace("../../", "")
    image_url = urljoin(BASE_SITE_URL, image_url)

    # Retourne les données sous forme de dictionnaire
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

    # Récupère toutes les pages de la catégorie (pagination)
    while url:
        print(f"  Page: {url}")
        books, url = get_books_from_page(url)
        book_urls.extend(books)

    books_data = []

    # Préparation du dossier d’images par catégorie
    safe_category = category_name.lower().replace(" ", "_")
    image_folder = os.path.join(output_folder, "images", safe_category)
    os.makedirs(image_folder, exist_ok=True)

    # Scrape chaque livre un par un avec une barre de progression
    for book_url in tqdm(book_urls, desc=f"  → Livres {category_name}"):
        try:
            book_data = scrape_product(book_url)  # Scraping des données
            books_data.append(book_data)

            # Téléchargement de l'image avec nom nettoyé
            image_filename = clean_filename(book_data["title"])[:100] + ".jpg"
            image_path = os.path.join(image_folder, image_filename)
            download_image(book_data["image_url"], image_path)

        except Exception as e:
            print(f"Erreur lors du scraping de {book_url} : {e}")

    return books_data  # Retourne toutes les données des livres de la catégorie
