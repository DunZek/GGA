import requests
import urllib.request
import time
from bs4 import BeautifulSoup as BS

url = "https://learn.sait.ca/d2l/le/calendar/6605?ou=6605"
response = requests.get(url)
print(response)
soup = BS(response.text, "html.parser")
tag = soup.find(class_="d2l-le-calendar-event")
print(type(soup))
for el in soup:
    print(type(el))
