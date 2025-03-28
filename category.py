import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import os

# Fonction : Récupération des URLs de livres sur une page
def get_books_from_page(url):
    response = requests.get(url)  # Envoie une requête à la page
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse le HTML de la page
    books = []

    # Parcours chaque livre sur la page
    for article in soup.select(".product_pod"):
        # Reconstitue l'URL complète du livre
        book_url = "https://books.toscrape.com/catalogue/" + article.h3.a["href"].replace("../../../", "")
        books.append(book_url) # Ajoute à la liste

    return books, soup.select_one(".next a") # Retourne les URLs des livres et le lien vers la page suivante (s’il existe)

# Fonction : Scraper les détails d’un livre
def scrape_product(url): 
    response = requests.get(url)
    response.raise_for_status()  # Lève une exception si la requête échoue
    response.encoding = "utf-8" # Forçage de l'utf-8
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraction des différentes informations du livre
    product_page_url = url
    upc = soup.find("th", string="UPC").find_next("td").text
    title = soup.find("h1").text
    price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    number_available = soup.find("th", string="Availability").find_next("td").text.strip()
    
    # Description du produit, si elle existe
    product_description = soup.find("meta", {"name": "description"})
    product_description = product_description["content"].strip() if product_description else ""
    
    # Catégorie du livre
    category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].text.strip()
    
    # Note du livre (par ex. One, Two, Three...)
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    
    # Reconstitution de l’URL de l’image
    image_url = soup.find("div", class_="item active").find("img")["src"].replace("../../", "")
    image_url = url.rsplit("/", 3)[0] + "/" + image_url.strip("/")

    # Retourne les données sous forme de dictionnaire
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

# Fonction : Scraper tous les livres d'une catégorie
def scrape_books(base_url, start_url):
    book_urls = []  # Liste de toutes les URLs des livres à scraper
    url = start_url

    # Boucle sur toutes les pages de la catégorie
    while url:
        print(f"Scraping page: {url}")
        page_books, next_page = get_books_from_page(url)
        book_urls.extend(page_books)

        # Si une page suivante existe, construit son URL
        if next_page:
            url = base_url + next_page["href"]
        else:
            url = None # Fin de la pagination

    books_data = [] # Stockage des données des livres
    print(f"\nScraping des détails de {len(book_urls)} livres en cours...\n")
    
    # Boucle sur tous les livres avec une barre de progression
    for book_data in tqdm(book_urls, desc="Progression", unit="livre"):
        books_data.append(scrape_product(book_data))

    return books_data # Retourne les données

# Fonction : Sauvegarde dans un fichier CSV
def save_to_csv(books, filename):
    if books:
        fieldnames = books[0].keys() # Récupère les en-têtes à partir du premier livre
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader() # Écrit l’en-tête
            writer.writerows(books) # Écrit les lignes du fichier

# Point d’entrée principal du script
if __name__ == "__main__":

    # L'utilisateur confirme s’il souhaite lancer le scraping
    start = input("Voulez-vous démarrer le scraping ? (o/n) : ").strip().lower()
    if start != "o":
        print("Scraping annulé.")
        exit()

    # Demande à l'utilisateur le dossier de sortie
    chemin_dossier = input("Où voulez-vous créer le dossier de sortie ? (ex: C:/Users/VotreNom/Documents ou ./ pour le dossier courant) : ").strip()
    nom_dossier = input("Quel nom souhaitez-vous donner à ce dossier ? : ").strip()

    chemin_complet = os.path.join(chemin_dossier, nom_dossier)

    # Création du dossier s’il n’existe pas
    if not os.path.exists(chemin_complet):
        os.makedirs(chemin_complet)
        print(f"Dossier '{chemin_complet}' créé avec succès.")
    else:
        print(f"Le dossier '{chemin_complet}' existe déjà.")

    # URL de base de la catégorie à scraper
    BASE_URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"
    START_URL = BASE_URL + "index.html"

    books_data = scrape_books(BASE_URL, START_URL)

    # Sauvegarde des données dans un fichier CSV
    chemin_fichier = os.path.join(chemin_complet, "books.csv")
    save_to_csv(books_data, chemin_fichier)
    print(f"Scraping terminé. Données enregistrées dans '{chemin_fichier}'")
