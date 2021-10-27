# Web automation
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Web scraping
from bs4 import BeautifulSoup as BS
import requests
import json

# Decision making
import datetime

# Headless
chrome_options = Options()
# chrome_options.add_argument('--headless')

# webdriver using services
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = s, options=chrome_options)

# SAIT login
driver.get("https://learn.sait.ca/d2l/login")

# Username
username = driver.find_element(By.XPATH, '//input[@id="username"]')
username.click()
username.send_keys("000872370")

# Password
password = driver.find_element(By.XPATH, '//input[@id="password"]')
password.click()
password.send_keys("0001035321")

# Sign In
signin = driver.find_element(By.XPATH, '//button[@type="submit"]')
signin.click()

# Calendar
calendar = driver.find_element(By.XPATH, '//a[@href="https://learn.sait.ca/d2l/le/calendar/6605?ou=6605"]')
calendar.click()

# Extract HTML starting from September, ending to December
month_number = int(datetime.datetime.now().strftime("%m"))
backwards = driver.find_element(By.XPATH, '//*[@id="DateSelectorIteratorId"]/a[1]')
forwards = driver.find_element(By.XPATH, '//*[@id="DateSelectorIteratorId"]/a[2]')
# Go back (month_number - 9) times to extract HTML starting from September
for n in range(month_number - 9):
    backwards.click()
    month_heading = driver.find_element(By.XPATH,'//*[@id="TitlePlaceholderId"]/div[1]/div[1]/h2')
# Extract HTML
for n in range(4):  # 4, a digit for each month -> September, October, November, December
    response = requests.get(driver.current_url)
    soup = BS(response.content, 'html.parser')
    forwards.click()

# Close
time.sleep(2)
driver.close()