import csv
import os

def save_to_csv(books, category_name, output_folder):
    if not books:
        return

    safe_category = category_name.lower().replace(" ", "_")
    filename = f"books_{safe_category}.csv"
    filepath = os.path.join(output_folder, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    print(f"Données sauvegardées dans : {filepath}")
