import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# URL de la première page de la catégorie
BASE_URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"
SITE_URL = "https://books.toscrape.com/catalogue/"

# Fonction pour extraire les URLs des pages produit
def extract_book_urls(base_url):
    book_urls = []
    page_url = base_url + "index.html"
    
    while page_url:
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de la page: {page_url}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Trouver tous les liens des livres
        for h3 in soup.find_all("h3"):
            a_tag = h3.find("a")
            if a_tag and "href" in a_tag.attrs:
                relative_url = a_tag["href"].replace("../../../", "")  # Corriger l'URL relative
                book_url = urljoin(SITE_URL , relative_url)
                book_urls.append(book_url)
                print(book_url)
        
        # Vérifier la présence du bouton "next" et construire la nouvelle URL
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page = next_button.find("a")["href"]
            page_url = urljoin(base_url, next_page)
        else:
            page_url = None
    
    return book_urls

# Extraction des URLs
data = extract_book_urls(BASE_URL)

# Enregistrement dans un fichier CSV
csv_filename = "../book_urls.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Product URL"])
    for url in data:
        writer.writerow([url])

print(f"Extraction terminée. Les URLs ont été enregistrées dans {csv_filename}")
