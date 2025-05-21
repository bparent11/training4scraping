from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # get element
from selenium.webdriver.common.keys import Keys # simulating touch of the keyboard

from selenium.webdriver.support.ui import WebDriverWait # let the driver wait for an element on the page
from selenium.webdriver.support import expected_conditions as EC # conditions to respect before go throught a WebDriverWait element
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import traceback

import time
import csv

# variables declaration

city_to_look_for = ["Metz", "Nancy", "Saint-Avold", "Sarreguemines"]
webdriverwaiting_seconds = 3
SCROLL_PAUSE_TIME = 2 # adjust according to the quality of the wifi connection, also depends on the fact that you're in full screen or not (e.g if you can display 4, 3 or 2,.. videos at once)
scroll_increment = 500  # pixels, we need it to not be too high to let all of the video duration get loaded

service_provider = []
designations = []
locations = []
# full ?

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

place_input = "saint-avold"
query_input = "osteopathe"

page_number = 1

driver.get(f"https://www.doctolib.fr/search?location={place_input}&speciality={query_input}&page={page_number}")

time.sleep(1)

# refuse cookies
try:
    refuse_cookies_btn = WebDriverWait(driver, webdriverwaiting_seconds).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Refuser']]"))
    )
    refuse_cookies_btn.click()
except TimeoutException:
    print("Pas de bannière de cookies affichée, on continue.")
except Exception as NotFound:
    raise KeyError("Le bouton pour refuser les cookies n'a pas été trouvé") from NotFound

time.sleep(1.5) # let some time to the next page to appear

""""""
"""""""Landing on the result page"
""""""

# url at this time : https://www.doctolib.fr/search?location=saint-avold&speciality=osteopathe
# url of the next page : https://www.doctolib.fr/search?location=saint-avold&speciality=osteopathe&page=2

time.sleep(2) # even if we have a "WebDriverWait", the element can be found but without any data yet, so we need to be careful with it.

try:
    nb_of_results = int(WebDriverWait(driver, webdriverwaiting_seconds).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'résultats')]"))
    ).text[:-9])
except:
    raise KeyError("Script didn't find the number of results")

nb_of_pages = int(int(nb_of_results) / 20) + 1

for i in range(nb_of_pages):
    # fetching each practitioner's data on the current page
    try:
        """Fetching NAMES"""
        names = driver.find_elements(By.CSS_SELECTOR, "h2.dl-text-bold")
        page_names = [name.text for name in names]

        """Fetching DESIGNATIONS"""
        cards = driver.find_elements(By.CSS_SELECTOR, "div.dl-card-content") # l'erreur précédent, moi j'avais pris les classes "flex flex-col w-full" pcq ct un parent très proche de p, et donc je me suis dis que ct la bonne solution de se mettre au plus proche. Mais justement non, le mieux c'est d'englober poursûr la chose que l'on cherche, et ensuite on va en profondeur.
        
        page_designations = []
        
        for card in cards:
            try:
                # look for all the p element in each card
                p_elements = card.find_elements(By.TAG_NAME, "p")
                for p in p_elements:
                    text = p.text.strip()
                    # filtering adresses
                    if len(text) < 60 and not any(char.isdigit() for char in text): # = aucun chiffre n'est présent dans le texte
                        page_designations.append(text)
                        break
            except NoSuchElementException:
                continue

        """Fetching LOCATIONS"""
        cards = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-wrap.gap-x-4")
        page_locations = [card.text.replace('\n', ' ') for card in cards if "conventionné" not in card.text.lower()] # the verification with "conventionné" could be an issue if I want to extend the usefulness of this script

        # saving the data
        assert (len(page_names) == len(page_designations)) and (len(page_designations) == len(page_locations))

        for j in range(len(page_names)):
            service_provider.append(page_names[j])
            designations.append(page_designations[j])
            locations.append(page_locations[j])

        page_number = (i+2)
        driver.get(f"https://www.doctolib.fr/search?location={place_input}&speciality={query_input}&page={page_number}")

        print(f"Page {page_number-1} has been successfully scraped !")
        time.sleep(12)

    except Exception as e:
        print("Erreur :", e)
        traceback.print_exc()

assert (len(service_provider) == len(designations)) and (len(designations) == len(locations))
assert len(service_provider) == nb_of_results

if 0==0:
    with open("Projets/doctolib_content.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["nom", "désignation", "adresse"])
        for i in range(len(service_provider)):
            row = [service_provider[i], designations[i], locations[i]]
            writer.writerow(row)

time.sleep(10)
driver.quit()