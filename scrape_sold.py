import requests
from bs4 import BeautifulSoup
import time

base_url = r"https://www.etsy.com/de/shop/BullwoodDE/sold"

# Schleife durchlaufen von 1 bis 6 für die Pagination
for page_number in range(1, 7):
    # URL mit aktueller Paginierungsnummer erstellen
    url = f'{base_url}?ref=pagination&page={page_number}'

    # Eine GET-Anfrage an die URL senden und den HTML-Inhalt erhalten
    response = requests.get(url)

    # Prüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Den HTML-Inhalt der Webseite in BeautifulSoup laden
        soup = BeautifulSoup(response.content, 'html.parser')

        # Alle <h3>-Tags mit dem Wort "listing" im id-Attribut finden
        listing_h3_tags = soup.find_all('h3', id=lambda x: x and 'listing' in x)

        # Die gefundenen <h3>-Tags ausgeben
        print(f"=== Seite {page_number} ===")
        for tag in listing_h3_tags:
            print(tag.text.strip())
    else:
        # Fehlermeldung ausgeben, falls die Anfrage nicht erfolgreich war
        print(f'Fehler beim Abrufen der Webseite {url}:', response.status_code)
    
    time.sleep(60)