import requests

url = "https://books.toscrape.com/"
page = requests.get(url)

# Voir le code html source
print(page.content)