from selenium import webdriver
import time

# Erstelle eine Option, um die bevorzugte Sprache einzustellen
options = webdriver.FirefoxOptions()
options.set_preference('intl.accept_languages', 'de-DE')

with webdriver.Firefox(options=options) as driver:

    # Webseite aufrufen
    driver.get('https://www.etsy.com/de/shop/BullwoodDE/sold')

    # Cookiemeldung akzeptieren und 2 sek warten
    btn_akzeptieren = driver.find_element("xpath", "/html/body/div[8]/div[2]/div/div[2]/div/div[2]/div[2]/button")
    btn_akzeptieren.click()
    time.sleep(2)

    # Öffnen der Datei zum Schreiben
    with open('bullwood.txt', 'w', encoding='utf-8') as file:

        # Alle h3-Tags abrufen, deren id-Attribut das Wort "listing" enthält
        for i in range(1, 2):
            # Url anpassen
            url = f'https://www.etsy.com/de/shop/BullwoodDE/sold?ref=pagination&page={i}'

            try:
                # Ausgabe in Konsole über Status
                print(f"Rufe Seite {i} ab...")

                # Webseite aufrufen
                driver.get(url)

                # Alle h3-Tags abrufen
                listing_h3_tags = driver.find_elements("xpath", "//h3[contains(@id, 'listing')]")

                # Schreiben der Texte der gefundenen h3-Tags in die Datei
                for tag in listing_h3_tags:
                    file.write(tag.text + '\n')

            except Exception as e:
                # Schreiben der Fehlermeldung in die Datei
                file.write(f'Fehler beim Abrufen von {url}: {str(e)}\n')

print("Done.")
