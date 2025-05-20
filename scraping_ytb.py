from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # get element
from selenium.webdriver.common.keys import Keys # simulating touch of the keyboard

from selenium.webdriver.support.ui import WebDriverWait # let the driver wait for an element on the page
from selenium.webdriver.support import expected_conditions as EC # conditions to respect before go throught a WebDriverWait element

import time

import csv

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.youtube.com/@morpheus-formation")

time.sleep(1)

try:
    accept_cookies_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Tout refuser']]"))
    )
    accept_cookies_btn.click()
except:
    raise KeyError("Le bouton pour refuser les cookies n'a pas été trouvé")

try:
    videos_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//yt-tab-shape[@tab-title='Vidéos']")) # élément yt-tab-shape qui *contient* "Vidéos"
    )
    videos_tab.click()
except:
    raise KeyError("Le bouton pour accéder aux vidéos n'a pas été trouvé")

time.sleep(2)

# scroll, scroll, scroll ...

titles = []
ytb_links = []
nb_views = []
pub_dates = []
durations = []

# Scrolling until all the videos are loaded
SCROLL_PAUSE_TIME = 2.5 # adjust according to the quality of the wifi connection, also depends on the fact that you're in full screen or not (e.g if you can display 4, 3 or 2,.. videos at once)
scroll_increment = 400  # pixels, we need it to not be too high to let all of the video duration get loaded

last_height = driver.execute_script("return document.body.scrollHeight")

# issue with the verification new_height = last_height, so I use a constant number of scrolls
iteration = 0
while iteration != 50:
    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    time.sleep(SCROLL_PAUSE_TIME)
    iteration += 1

videos = driver.find_elements(By.ID, "content")

for i in range(len(videos)):
    video_title_link_ID = videos[i].find_element(By.ID, "video-title-link")

    """Titres"""
    titles.append(video_title_link_ID.text)

    """YTB LINK"""
    ytb_links.append(video_title_link_ID.get_attribute("href"))
    
    """Views counter and Publication date"""
    metadata = WebDriverWait(videos[i], 10).until(
        EC.presence_of_element_located((By.ID, "metadata-line"))
    )
    # Récupère toutes les balises <span> dans ce bloc
    spans = metadata.find_elements(By.TAG_NAME, "span")
    nb_views.append(spans[0].text)
    pub_dates.append(spans[1].text)

    """Duration"""
    durations.append(videos[i].find_element(By.CLASS_NAME, "badge-shape-wiz__text").text)

    if (i % 50) == 0:
        print(f"{i+1} / {len(videos)} done !")

if 0==0:
    with open("Projets/morpheus_content_long.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["title", "nb_views", "publication_date", "duration", "ytb_link", "video_type"])
        for i in range(len(titles)):
            row = [titles[i], nb_views[i], pub_dates[i], durations[i], ytb_links[i], "long"]
            writer.writerow(row)

time.sleep(1)
driver.quit()