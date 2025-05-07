import requests
import os

def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url} : {e}")
