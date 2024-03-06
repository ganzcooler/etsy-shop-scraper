from selenium import webdriver
import time
import os
import matplotlib.pyplot as plt

# Erstelle eine Option, um die bevorzugte Sprache einzustellen
options = webdriver.FirefoxOptions()
options.set_preference('intl.accept_languages', 'de-DE')

# Definiere den Pfad zum %localappdata%-Verzeichnis und zum Unterordner "etsy-scraper"
localappdata_path = os.environ.get('LOCALAPPDATA')
subfolder_path = os.path.join(localappdata_path, 'etsy-scraper')

# Erstelle den Unterordner "etsy-scraper", falls er nicht existiert
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

# Definiere den Pfad zur Datei im Unterordner "etsy-scraper"
file_path = os.path.join(subfolder_path, 'bullwood_h3_tags.txt')

with webdriver.Firefox(options=options) as driver:

    # Webseite aufrufen
    driver.get('https://www.etsy.com/de/shop/BullwoodDE/sold')

    # Cookiemeldung akzeptieren und 2 Sekunden warten
    btn_akzeptieren = driver.find_element("xpath", "/html/body/div[8]/div[2]/div/div[2]/div/div[2]/div[2]/button")
    btn_akzeptieren.click()
    time.sleep(2)

    # Öffnen der Datei zum Schreiben im Unterordner "etsy-scraper"
    with open(file_path, 'w', encoding='utf-8') as file:

        # Alle h3-Tags abrufen, deren id-Attribut das Wort "listing" enthält
        all_h3_tags = []

        for i in range(1, 2):
            # URL anpassen
            url = f'https://www.etsy.com/de/shop/BullwoodDE/sold?ref=pagination&page={i}'

            try:
                # Ausgabe in Konsole über Status
                print(f"Rufe Seite {i} ab...")

                # Webseite aufrufen
                driver.get(url)

                # Alle h3-Tags abrufen
                listing_h3_tags = driver.find_elements("xpath", "//h3[contains(@id, 'listing')]")

                # Hinzufügen der Texte der gefundenen h3-Tags zur Liste
                all_h3_tags.extend(tag.text for tag in listing_h3_tags)

                # Schreiben der Texte der gefundenen h3-Tags in die Datei
                for tag in listing_h3_tags:
                    file.write(tag.text + '\n')

            except Exception as e:
                # Schreiben der Fehlermeldung in die Datei
                file.write(f'Fehler beim Abrufen von {url}: {str(e)}\n')

# Erstelle Histogramm der h3-Tags mit Matplotlib
tag_histogram = {}

for tag in all_h3_tags:
    tag_histogram[tag] = tag_histogram.get(tag, 0) + 1

# Sortieren des Histogramms nach Anzahl der Vorkommen
sorted_histogram = dict(sorted(tag_histogram.items(), key=lambda item: item[1], reverse=True))

# Aufteilung der Daten für das Histogramm
tags = list(sorted_histogram.keys())
counts = list(sorted_histogram.values())

# Erstellung des Histogramms
plt.bar(tags[:10], counts[:10])  # Nur die ersten 10 Tags anzeigen
plt.xlabel('Tags')
plt.ylabel('Anzahl')
plt.title('Histogramm der h3-Tags (Top 10)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Anzeigen des Histogramms
plt.show()

print("Done.")
