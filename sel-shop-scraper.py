from selenium import webdriver
import time
import os
from datetime import datetime

# Get shop url
url = input()
if not url.endswith("sold"):
    raise ValueError("Falsche Shop-URL")
start_index = url.find("shop/") + len("shop/")
end_index = url.find("/", start_index)
shop_name = url[start_index:end_index]

# Erstelle eine Option, um die bevorzugte Sprache einzustellen
options = webdriver.FirefoxOptions()
options.set_preference('intl.accept_languages', 'de-DE')

# Erstelle den Unterordner mit shop-name, falls er nicht existiert
current_directory = os.getcwd()
subfolder_path = os.path.join(current_directory, shop_name)
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

# Erstelle einen Dateinamen mit Zeitstempel
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
enumeration_file_name = f"{current_time}_{shop_name}_products.txt"
enumeration_file_path = os.path.join(subfolder_path, enumeration_file_name)

with webdriver.Firefox(options=options) as driver:

    # Webseite aufrufen
    driver.get(url)

    # Cookiemeldung akzeptieren und 2 Sekunden warten
    btn_akzeptieren = driver.find_element("xpath", "/html/body/div[8]/div[2]/div/div[2]/div/div[2]/div[2]/button")
    btn_akzeptieren.click()
    time.sleep(2)

    # Alle h3-Tags abrufen, deren id-Attribut das Wort "listing" enthält
    all_h3_tags = []

    for i in range(1, 7):
        # URL anpassen
        url = f'{url}?ref=pagination&page={i}'

        try:
            # Ausgabe in Konsole über Status
            print(f"Rufe Seite {i} ab...")

            # Webseite aufrufen
            driver.get(url)

            # Alle h3-Tags abrufen
            listing_h3_tags = driver.find_elements("xpath", "//h3[contains(@id, 'listing')]")

            # Hinzufügen der Texte der gefundenen h3-Tags zur Liste
            all_h3_tags.extend(tag.text for tag in listing_h3_tags)

        except Exception as e:
            # Fehlermeldung in die Konsole ausgeben
            print(f'Fehler beim Abrufen von {url}: {str(e)}')

# Sortieren der Tags nach der Anzahl der Vorkommen
tag_counts = {}
for tag in all_h3_tags:
    tag_counts[tag] = tag_counts.get(tag, 0) + 1

# Tags absteigend nach Häufigkeit sortieren
sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

# Schreibe die aufgezählten Tags in die separate Datei
with open(enumeration_file_path, 'w', encoding='utf-8') as enumeration_file:
    for tag, count in sorted_tags:
        enumeration_file.write(f"{tag}: {count}\n")

# Schreibe die h3-Tags in die Datei im aktuellen Verzeichnis
with open(file_path, 'w', encoding='utf-8') as file:
    for tag in all_h3_tags:
        file.write(tag + '\n')

print("Done.")
