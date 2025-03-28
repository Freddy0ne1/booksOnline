# Instructions d'utilisation - Books to Scrape

Le script "all_categories.py" permet de scraper automatiquement les livres du site [Books to Scrape](https://books.toscrape.com), télécharger leurs images et sauvegarder les données dans des fichiers CSV organisés par catégorie.

---

## Fonctionnalités

  - Scraping de **toutes les catégories** du site.
  - Extraction des **données détaillées** de chaque livre :
  - Titre
  - Prix (HT / TTC)
  - Stock disponible
  - Description
  - Catégorie
  - Note (rating)
  - UPC (code produit)
  - URL de la page et de l'image
  - Enregistrement dans des fichiers CSV par catégorie.
  - Téléchargement des **images de couverture** pour chaque livre.
  - **Barre de progression** pour visualiser l'avancement avec `tqdm`.
  - Gestion des erreurs réseau et des titres de fichiers non valides.

---

## Prérequis

Avant d'exécuter le script, il faut d'abord créer un environnement virtuel et l'activer avec les commandes ci-dessous

Pour le créer : 
python -m venv env

Pour l'activer :
source env/scripts/activate

## Installation de librairies 

Pour installer les librairies :
pip install -r requirements.txt


## Pour lancer le scraping

Pour exécuter le script, il suffit de lancer :
python main.py

## Interactivité

Lorsque de l'exécution du script, une question simple est posée :
 **Voulez-vous démarrer le scraping ? (o/n)**

Choix du dossier de destination : 
Si l’utilisateur accepte, le script lui demande où enregistrer les résultats, avec deux questions faciles

Où voulez-vous créer le dossier de sortie ? : Pour ne pas enregistrer à la racine du script, utilisez ce type de chemin ("../mon_dossier")

Quel nom voulez-vous donner au dossier ?