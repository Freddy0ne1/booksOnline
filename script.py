import requests
from bs4 import BeautifulSoup
import csv

# URL du livre
url = "https://books.toscrape.com/catalogue/emma_17/index.html"

# Lancer la requête HTTP
reponse = requests.get(url)
page = reponse.content

soup = BeautifulSoup(page, "html.parser")

# Extraire le titre
titres = soup.find("h1")
titre_textes = []
for titre in titres:
    titre_textes.append(titre.string)

# Extraire le prix
prix = soup.find("p", class_="price_color")
prix_textes = []
for prix in prix:
    prix_textes.append(prix.string)

# Extraire la disponibilité
disponibilites = soup.find("p", class_="instock availability")
disponibilite_textes = [disponibilites.get_text(strip=True)] if disponibilites else []

# Extraire la description
descriptions = soup.find("div", id="product_description")
description = descriptions.find_next_sibling("p").text.strip()

# Edition du fichier CSV
en_tete = ["titre", "prix", "disponibilité", "description"]
with open("../data.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(en_tete)
    for titre, prix, disponibilite, in zip(titre_textes, prix_textes, disponibilite_textes):
        writer.writerow([titre, prix, disponibilite, description])
