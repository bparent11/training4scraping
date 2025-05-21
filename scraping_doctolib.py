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
webdriverwaiting_seconds = 10
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

driver.get(f"https://www.doctolib.fr/search?location={place_input}&speciality={query_input}")

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

# finally useless because you can access it easily with the url

# access to the query input (search bar)
#try:
#    query_INPUT = WebDriverWait(driver, webdriverwaiting_seconds).until(
#        EC.presence_of_element_located((By.CLASS_NAME, "searchbar-query-input"))
#    )
#    query_INPUT.clear()
#    query_INPUT.send_keys("Ostéopathe")
#except:
#    raise KeyError("Script didn't find the query input.")
#
## access to the place input (search bar)
#try:
#    place_INPUT = WebDriverWait(driver, webdriverwaiting_seconds).until(
#        EC.presence_of_element_located((By.CLASS_NAME, "searchbar-place-input"))
#    )
#    place_INPUT.clear()
#    place_INPUT.send_keys("Saint-Avold")
#    time.sleep(0.5) # let the time to the drop-down list to appear
#    place_INPUT.send_keys(Keys.ENTER + Keys.ENTER)
#except:
#    raise KeyError("Script didn't find the place input.")


""""""
"""""""Landing on the result page"
""""""


# url at this time : https://www.doctolib.fr/search?location=saint-avold&speciality=osteopathe
# url of the next page : https://www.doctolib.fr/search?location=saint-avold&speciality=osteopathe&page=2

time.sleep(2) # even if we have a "WebDriverWait", the element can be found but without any data yet, so we need to be careful with it.

try:
    nb_of_results = WebDriverWait(driver, webdriverwaiting_seconds).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'résultats')]"))
    ).text[:-9]
except:
    raise KeyError("Script didn't find the number of results")

print(nb_of_results)
nb_of_pages = int(int(nb_of_results) / 20) + 1


# fetching each practitioner's data
try:
    """Fetching NAMES"""
    names = driver.find_elements(By.CSS_SELECTOR, "h2.dl-text-bold")
    page_names = [name.text for name in names]

    """Fetching DESIGNATIONS"""
    cards = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.w-full")
    page_designations = []
    i=0
    for card in cards:
        try:
            p_elem = card.find_element(By.TAG_NAME, "p")
            if i<2: # because the 2 elements which aren't practioners' data are fetched by this (no other solution)
                pass
            else:
                page_designations.append(p_elem.text)
            i+=1
        except NoSuchElementException:
            pass

    """Fetching LOCATIONS"""
    cards = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-wrap.gap-x-4")
    page_locations = [card.text.replace('\n', ' ') for card in cards if "conventionné" not in card.text.lower()]

except Exception as e:
    print("Erreur :", e)
    traceback.print_exc()

time.sleep(10)
driver.quit()