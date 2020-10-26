from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup
import constants
import time
import os


def introduction():
    print("Hello, welcome to the Newegg.com web-scraper")
    time.sleep(2)
    print("Using this web-scraper you can search up your favourite products, getting real time data.")
    time.sleep(2.5)
    print("For your convenience we have gone ahead and created some optional category's for you to try. \nBut don't feel hindered. You can search up whatever you want!")
    time.sleep(4)
    print("Some possible category's include but are not limited to - Graphics cards, Ram, PC cases and storage.")
    time.sleep(2)


def input_code():
    while True:
        user_input = input("Please enter a keyword(s) to search newegg.com: ")
        try:
            _ = int(user_input)
        except ValueError:
            pass
        else:
            print("Please do not enter numbers!")
            continue
        user_search = user_input.replace(' ', '+')
        input_validate = user_input
        misspelled = constants.SPELL.unknown(input_validate.split())
        if len(input_validate) >= 30:
            print("Please enter a shorter message.")
            continue
        elif len(input_validate.split()) > 3:
            print("Please type no more than 4 words")
            continue
        elif misspelled == set():
            print("Searching newegg.com for " + user_input)
            return [user_search, user_input]
        else:
            print("Please enter a word in the english dictionary. \nThe word '" + user_input + "' is not valid")


def timer(timer_var):
    while True:
        time.sleep(1)
        timer_var = timer_var - 1
        print(timer_var)
        if timer_var == 0:
            break
        else:
            continue


def web_scraper():
    while True:
        user_input = input_code()
        user_url = user_input[0]
        user_search = user_input[1]

        print(user_search)

        url = constants.LINK + user_url

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
        container = "none"

        # prototyping a for loop that basically goes through the page as I will do something like "for every container in containers
        try:
            container = containers[0]
            break
        except Exception:
            print("I'm sorry. There are no search results for '" + user_search + "'. \nPlease wait 10 seconds before searching again to prevent excessive traffic")
            timer(11)
            return [container, containers]


def file_write():
    container = web_scraper()

    filename = "products.csv"
    file = open(filename, "w")

    headers = "Brand, Product name, Price, Original price, Rating, Additional promotions\n"

    file.write(headers)

    # creating the loop
    for container[0] in container[1]:
        try:
            rating_container = container[0].findAll("a", {"class": "item-rating"})
            rating = str(rating_container[0]["title"])
            rating = [int(s) for s in rating.split() if s.isdigit()]
        except Exception:
            rating = "none"

        try:
            origin_price_container = container[0].findAll("li", {"class": "price-was"})
            origin_price = origin_price_container[0].text
        except IndexError:
            origin_price = "none"

        try:
            model = container[0].img["alt"]
        except KeyError:
            model = "none"

        try:
            price_container = container[0].findAll("li", {"class": "price-current"})
            price = price_container[0].text
        except IndexError:
            price = "none"

        try:
            brand_container = container[0].findAll("a", {"class": "item-brand"})
            brand = brand_container[0].img["alt"]
        except IndexError:
            brand = "none"

        try:
            promotion = container[0].div.p.text
        except AttributeError:
            promotion = "none"

        file.write(str(brand) + "," + str(model.replace(",", "|")) + "," + str(price) + "," + str(origin_price) + "," + str(rating) + "/[5]," + str(promotion.replace(",", "-")) + "\n")

    file.close()

    print("Search finished! Thank you for using the newegg.com web-scraper. \nYour results have been written to a CSV file! \nYour CSV file is called " + filename + "! Your file directory is: \n" + os.getcwd() + "\\products.csv")


container = web_scraper()


print(container)


