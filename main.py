# === Import des modules nécessaires ===
import os  # Pour manipuler les dossiers et chemins de fichiers

# Import des fonctions du projet (modules internes)
from categories import get_all_categories  # Récupère toutes les catégories disponibles sur le site
from book_scraper import scrape_books_from_category  # Scrape les livres d'une catégorie donnée
from data_saver import save_to_csv  # Enregistre les données dans un fichier CSV


def main():
    """
    Fonction principale qui orchestre le scraping :
    - Interaction avec l'utilisateur
    - Création du dossier de sortie
    - Scraping des livres par catégorie
    - Sauvegarde des données dans des fichiers CSV
    """
    
    # Demande à l'utilisateur s'il souhaite lancer le scraping
    start = input("Voulez-vous démarrer le scraping ? (o/n) : ").strip().lower()
    if start != "o":
        print("Scraping annulé.")
        return  # Interrompt le programme si l'utilisateur répond autre chose que "o"


    # Répertoire parent par défaut (à la racine du projet)
    chemin_dossier = "../"

    # Nom du dossier de sortie (fourni par l'utilisateur)
    nom_dossier = input("Quel nom voulez-vous donner au dossier de sortie ? : ").strip()

    # Construction du chemin complet de sortie
    chemin_complet = os.path.join(chemin_dossier, nom_dossier)

    # Création du dossier si nécessaire
    if not os.path.exists(chemin_complet):
        os.makedirs(chemin_complet)
        print(f"Dossier '{chemin_complet}' créé avec succès.")
    else:
        print(f"Le dossier '{chemin_complet}' existe déjà.")

    # Récupération de toutes les catégories disponibles sur le site
    categories = get_all_categories()

    # Pour chaque catégorie, lancer le scraping et sauvegarder les données
    for category_name, category_url in categories.items():
        books_data = scrape_books_from_category(category_name, category_url, chemin_complet)
        save_to_csv(books_data, category_name, chemin_complet)


        # Message final une fois que tout le scraping est terminé
    print("\nScraping terminé pour toutes les catégories.")


# Point d’entrée du programme si ce fichier est exécuté directement
if __name__ == "__main__":
    main()
