from selenium import webdriver

with webdriver.Firefox() as driver:

    # Webseite aufrufen
    driver.get('https://www.etsy.com/de/shop/BullwoodDE/sold')

    # cookiemeldung akzeptieren
    btn_akzeptieren = driver.find_element("xpath", "/html/body/div[8]/div[2]/div/div[2]/div/div[2]/div[2]/button")
    btn_akzeptieren.click()

    # Alle h3-Tags abrufen, deren id-Attribut das Wort "listing" enthält
    listing_h3_tags = driver.find_elements("xpath", "//h3[contains(@id, 'listing')]")

    # Ausgabe der Texte der gefundenen h3-Tags
    for tag in listing_h3_tags:
        print(tag.text)

# Webdriver schließen
driver.quit()