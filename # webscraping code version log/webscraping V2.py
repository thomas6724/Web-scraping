import csv
import requests
from bs4 import BeautifulSoup
result = requests.get("https://www.google.com/")
print("Results: " + result.status_code)
print(result.headers)
src = result.content
soup = BeautifulSoup(src, "lxml")
links = soup.findall('a')
print(links)
print("\n")