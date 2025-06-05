import csv  # Pour écrire dans des fichiers CSV
import os   # Pour manipuler les chemins de fichiers et dossiers

def save_to_csv(books, category_name, output_folder):
    """
    Sauvegarde les données d'une liste de livres dans un fichier CSV.
    
    Paramètres :
    - books : liste de dictionnaires contenant les infos de chaque livre
    - category_name : nom de la catégorie (utilisé pour nommer le fichier)
    - output_folder : chemin du dossier où enregistrer le fichier
    """
    
    # Si la liste des livres est vide, on ne fait rien
    if not books:
        return

    # Préparation du nom de fichier : nom de catégorie nettoyé
    safe_category = category_name.lower().replace(" ", "_")
    filename = f"books_{safe_category}.csv"

    # Construction du chemin complet du fichier CSV
    filepath = os.path.join(output_folder, filename)

    # Ouverture du fichier en écriture (w), avec encodage UTF-8
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        # Création d’un writer CSV basé sur les clés du premier dictionnaire
        writer = csv.DictWriter(file, fieldnames=books[0].keys())

        # Écrit la ligne d’en-tête (colonnes)
        writer.writeheader()

        # Écrit toutes les lignes de livres
        writer.writerows(books)

    # Message de confirmation en console
    print(f"Données sauvegardées dans : {filepath}")
