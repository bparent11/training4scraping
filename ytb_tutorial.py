from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # get element
from selenium.webdriver.common.keys import Keys # simulating touch of the keyboard

from selenium.webdriver.support.ui import WebDriverWait # let the driver wait for an element on the page
from selenium.webdriver.support import expected_conditions as EC # conditions to respect before go throught a WebDriverWait element

import time

# https://sites.google.com/chromium.org/driver/

service = Service(executable_path="chromedriver.exe")

opts = Options()
opts.add_argument("--start-maximized")
opts.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(service=service)

driver.get("https://google.com/ncr") # ncr is useful to don't get the security page when you run the python file

# time.sleep(5) # sleeping time to let me accept cookies (i'll handle the automation of it later)

# operating a google search
try:
    accept_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "L2AGLb"))
    )
    accept_btn.click()
    time.sleep(1) # time sleep here to let the time to the search bar to appears and avoid an error

except:
    raise KeyError("Didn't find the accepting cookies button")

seconds = 10
try:
    WebDriverWait(driver, seconds).until( # wait for 5 seconds until something appears, if it doesn't, return an error
        EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
    )
    input_element = driver.find_element(By.CLASS_NAME, "gLFyf") # access to the search bar
    input_element.clear() # clear the element (the search bar here)
    input_element.send_keys("tech with tim" + Keys.ENTER) # append it in the search bar and search for it
except:
    raise KeyError("Didn't find the search bar")

# click on a link
link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim") # looking for the first link that contains "Tech With Tim" in this capitalisation
links = driver.find_elements(By.LINK_TEXT, "Tech With Tim") # looking for all the links that exactly correspond to "Tech With Tim"
link.click()

time.sleep(10)

driver.quit()