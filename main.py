import os
from categories import get_all_categories
from book_scraper import scrape_books_from_category
from data_saver import save_to_csv

def main():
    start = input("Voulez-vous démarrer le scraping ? (o/n) : ").strip().lower()
    if start != "o":
        print("Scraping annulé.")
        return

    chemin_dossier = "../"
    nom_dossier = input("Quel nom voulez-vous donner au dossier de sortie ? : ").strip()
    chemin_complet = os.path.join(chemin_dossier, nom_dossier)

    if not os.path.exists(chemin_complet):
        os.makedirs(chemin_complet)
        print(f"Dossier '{chemin_complet}' créé avec succès.")
    else:
        print(f"Le dossier '{chemin_complet}' existe déjà.")

    categories = get_all_categories()

    for category_name, category_url in categories.items():
        books_data = scrape_books_from_category(category_name, category_url, chemin_complet)
        save_to_csv(books_data, category_name, chemin_complet)

    print("\nScraping terminé pour toutes les catégories.")

if __name__ == "__main__":
    main()
