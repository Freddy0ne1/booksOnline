# **Books to Scrape - Instructions d'utilisation**  

Le script **`main.py`** permet de scraper automatiquement les livres du site [Books to Scrape](https://books.toscrape.com), de télécharger leurs images et de sauvegarder les données dans des fichiers CSV organisés par catégorie.  

---

## 🚀 **Fonctionnalités**  

✅ **Scraping de toutes les catégories** du site.  
✅ **Extraction des données détaillées** de chaque livre :  
   - 📌 **Titre**  
   - 💰 **Prix** (HT / TTC)  
   - 📦 **Stock disponible**  
   - 📝 **Description**  
   - 📂 **Catégorie**  
   - ⭐ **Note (rating)**  
   - 🔑 **UPC (code produit)**  
   - 🔗 **URL de la page et de l’image**  
✅ **Enregistrement des données** dans des fichiers CSV par catégorie.  
✅ **Téléchargement des images de couverture** pour chaque livre.  
✅ **Affichage d’une barre de progression** grâce à `tqdm`.  

---

## 🔧 **Prérequis**  

### 1️⃣ **Outils nécessaires**  
- **Visual Studio Code** (exemple d’utilisation basé sur cet éditeur) → [Téléchargement ici](https://code.visualstudio.com/download).  
- **Git Bash** installé sur l’ordinateur → [Téléchargement ici](https://git-scm.com/downloads).  

### 2️⃣ **Clonage du projet**  

Dans Visual Studio Code :  
1. Ouvrir l’explorateur de fichiers (Explorer).  
2. Clicker sur **clone Repository** et coller l'URL ci-dessous "repository source"  

   ```
   https://github.com/Freddy0ne1/booksOnline
      ```

Une fois l'URL collée, appuyer sur la touche Entrée et selectionner le dossier de destination pour cloner le projet.

3. Ouvrir la palette de commandes (**Ctrl + Maj + P**), rechercher **"Create New Terminal (With Profile)"**, puis sélectionner **"Git Bash"**.  

---

## 🛠️ **Installation des dépendances**  

### 1️⃣ **Créer et activer un environnement virtuel**  

Dans le terminal **Git Bash** sous Visual Studio Code, exécuter :  

```bash
# Code pour Windows 

# Création de l’environnement virtuel (Windows)
python -m venv env

# Activation de l’environnement (Windows)
source env/Scripts/activate

# Code pour linux

# Création de l’environnement virtuel (Linux)
python3 -m venv env

# Activation de l’environnement (Linux)
source env/bin/activate
```

### 2️⃣ **Installer les librairies nécessaires**  

```bash
pip install -r requirements.txt
```

---

## ▶️ **Lancer le scraping**  

Exécuter le script avec :  

```bash
python main.py
```

### 🛠 **Interactivité du script**  
Lors de l’exécution, deux questions seront posées :  

1. **Démarrer le scraping ?**  
   ```
   Voulez-vous démarrer le scraping ? (o/n)
   ```
2. **Nom du dossier de sortie**  
   ```
   Quel nom voulez-vous donner au dossier ?
   ```
