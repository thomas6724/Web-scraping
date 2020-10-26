from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup
import constants
import time
import sys


def input_code():
    while True:
        user_input = input("Please enter something to search: ")
        user_search = user_input.replace(' ', '+')
        print(user_search)
        if len(user_input) >= 30:
            print("Please enter a shorter message.")
            continue
        elif len(user_input.split()) > 3:
            print("Please type no more than 4 words")
            continue
        else:
            print("Please head to " + file_name + " to see the data. You can find this file in\n " + file_location)
            return [user_search, user_input]


def introduction():
    print("Hello, welcome to the Newegg.com web-scraper")
    time.sleep(2)
    print("Using this webscraper you can search up your favourite products, getting real time data.")
    time.sleep(2.5)
    print("For your convenience we have gone ahead and created some optional catagorys for you to try. \nBut don't feel hindered. You can search up whatever you want!")
    time.sleep(4)
    print("Some possible catagorys include but are not limited to - Graphics cards, Ram, PC cases and storage.")
    time.sleep(2)


introduction()

file_name = "test"
file_location = "test"

user_input = input_code()

print(user_input[1])

url = constants.LINK + constants.USER_URL #CREATE CONSTANT
random = "hi"
# opens the connection and downloads html page from url
uClient = url_req(url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
# putting it inside a variable to prevent the whole code crashing
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# Grabs each product
containers = page_soup.findAll("div", {"class": "item-container"})

# prototyping a for loop that basically goes through the page as I will do something like "for every container in containers
try:
    contain = containers[0]
    container = containers[0]
except Exception:
    print("I'm sorry. There are no search results for '" + constants.USER_SEARCH[1] + "'")
    sys.exit()

# creating the loop
for container in containers:
    try:
        rating_container = container.findAll("a", {"class": "item-rating"})
        rating = str(rating_container[0]["title"])
        rating = [int(s) for s in rating.split() if s.isdigit()]
    except Exception:
        rating = "none"

    try:
        origin_price_container = container.findAll("li", {"class": "price-was"})
        origin_price = origin_price_container[0].text
    except Exception:
        origin_price = "none"

    try:
        model = container.img["alt"]
    except Exception:
        model = "none"

    try:
        price_container = container.findAll("li", {"class": "price-current"})
        price = price_container[0].text
    except Exception:
        price = "none"

    try:
        brand_container = container.findAll("a", {"class": "item-brand"})
        brand = brand_container[0].img["alt"]
    except Exception:
        brand = "none"

    try:
        promotion = container.div.p.text
    except Exception:
        promotion = "none"

    print("Brand: " + brand)
    print("Price: " + price)
    print("Model: " + model)
    print("Original price: " + origin_price)
    print("Rating: " + str(rating) + "/[5]")
    print("Promotion: " + promotion)

