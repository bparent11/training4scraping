from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# https://sites.google.com/chromium.org/driver/

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com/ncr") # ncr is useful to don't get the security page when you run the python file

time.sleep(10)

driver.quit()