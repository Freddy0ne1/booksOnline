import requests  # Pour envoyer des requêtes HTTP (ici pour télécharger les images)
import os        # Pour manipuler les chemins de fichiers et créer des dossiers

def download_image(url, path):
    """
    Télécharge une image depuis une URL et l'enregistre à l'emplacement spécifié.

    Paramètres :
    - url : l’URL de l’image à télécharger
    - path : le chemin complet du fichier où enregistrer l’image
    """

    try:
        # Envoie une requête GET à l'URL de l'image avec le mode "stream" (flux)
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Déclenche une exception en cas d'erreur HTTP (404, 500, etc.)

        # Crée les répertoires nécessaires si le dossier de destination n’existe pas
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Ouvre le fichier en mode binaire pour l’écriture
        with open(path, "wb") as f:
            # Écrit l'image par blocs de 1024 octets
            for chunk in response.iter_content(1024):
                f.write(chunk)

    # En cas de problème de connexion, d’URL invalide, ou de serveur indisponible
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url} : {e}")
