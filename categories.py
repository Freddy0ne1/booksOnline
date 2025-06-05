# Importation des modules nécessaires
import requests  # Pour envoyer des requêtes HTTP
from bs4 import BeautifulSoup  # Pour parser et analyser le HTML
from urllib.parse import urljoin  # Pour combiner des URLs relatives avec une URL de base
from config import BASE_SITE_URL  # URL de base du site, stockée dans un fichier de configuration

def get_all_categories():
    """
    Récupère toutes les catégories de livres disponibles sur le site.
    Retourne un dictionnaire contenant le nom de chaque catégorie et son URL complète.
    """
    
    # Envoie une requête GET à la page d'accueil du site
    response = requests.get(BASE_SITE_URL)
    
    # Analyse le contenu HTML de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Sélectionne tous les éléments <a> correspondant aux catégories dans la barre latérale
    category_elements = soup.select("div.side_categories ul li ul li a")

    # Initialise un dictionnaire pour stocker les catégories
    categories = {}

    # Parcourt chaque élément de catégorie trouvé
    for cat in category_elements:
        name = cat.text.strip()  # Récupère le nom de la catégorie (en supprimant les espaces inutiles)
        href = cat["href"]  # Récupère le lien relatif vers la catégorie
        url = urljoin(BASE_SITE_URL, href)  # Construit l’URL absolue de la catégorie
        categories[name] = url  # Ajoute la catégorie au dictionnaire

    # Retourne le dictionnaire des catégories avec leur URL
    return categories
