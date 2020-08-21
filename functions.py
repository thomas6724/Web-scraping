from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup
import constants
import time
import sys
import os


def introduction():
    """
    Sends out a line of print statements set at intervals introducing the user to the web-scraper.
    """
    print("Hello, welcome to the Newegg.com web-scraper")

    # pauses program for 2 seconds
    time.sleep(2)
    print("Using this web-scraper you can search up your favourite products, getting real time data.")

    # pauses program for 2.5 seconds
    time.sleep(2.5)
    print("For your convenience we have gone ahead and created some optional category's for you to try.")

    # pauses program for 3 seconds
    time.sleep(3)
    print("But don't feel hindered. You can search up whatever you want!")

    # pauses program for 2 seconds
    time.sleep(2)
    print("Some possible category's include but are not limited to - Graphics cards, Ram, PC cases and storage.\n")

    # pauses program for 3 seconds
    time.sleep(3)


def input_code():
    """
    Takes input from the user, validates input and turns it into something usable for the end of a link.

    Returns
    -------
    user_search : str
        Takes user_input and replaces specific keystrokes with symbols turning the
        return into a form that works with links.
    user_input : str
        Takes input from the user.

    Raises
    ------
    ValueError
        Raises error verifying the user has only entered text.

    Notes
    -----
    os.system('cls') will only work on windows. If using a mac please change this line to os.system('clear')
    """
    while True:

        # user input
        user_input = input("Please enter a keyword(s) to search newegg.com: ")

        # clears the console on windows when not using pycharm
        os.system('cls')

        try:
            # checks to see if there is a number in input
            input_nospace = user_input.replace(" ", "")
            print(input_nospace)
            _ = int(input_nospace)

        # checks to see if the user has entered no numbers
        # accepts input
        except ValueError:
            pass
        else:
            print("Please do not enter numbers!")
            continue

        # SPELL is a constant
        # changes the user input into something url appropriate
        # checks if there is a spelling mistake in the input
        user_search = user_input.replace(' ', '+')
        misspelled = constants.SPELL.unknown(user_input.split())

        # checks if the user has typed anything
        # does not accept nothing
        if len(user_input.strip()) == 0 or len(user_input.strip()) == 1:
            print("Please put in a valid input!")
            continue

        # checks the input for character length
        # does not accept more than 30 characters
        if len(user_input) >= 30:
            print("Please enter a shorter message.")
            continue

        # checks the input for word count
        # does not accept more than 4 words
        elif len(user_input.split()) > 4:
            print("Please type no more than 4 words")
            continue

        # checks to see if there is a typo in a word
        # if there isn't it accepts the input
        elif misspelled == set():
            print("Searching newegg.com for " + user_input)

            # returns the input and search from the def
            return [user_search, user_input]

        # picks up all typos/ non english words and symbols
        else:
            print("Please enter a word in the english dictionary. \nThe word '" + user_input + "' is not valid")


def timer(timer_var):
    """
    A countdown per second to 0, whilst printing the seconds.

    parameters
    ----------
    timer_var : int, necessary
        Allows programmer to set different int values to start the countdown.
    """
    while True:
        # wait one second
        # minus one second off
        # repeat unless timer has reached 0
        time.sleep(1)
        timer_var = timer_var - 1
        print(timer_var)
        if timer_var == 0:
            break
        else:
            continue


def web_scraper():
    """
    Code that inputs your search into newegg.com search algorithm and then reads the results of said search.
    Further reads and writes the search results to a file.

    Returns
    -------
    file_name: str
        Returns the name of the CSV file that has been written to.

    Raises
    ------
    ValueError
        Input is not compatible.
    IndexError
        Raised when a list doesnt exist. Raised when the web-scraper finds no search results and
        cannot create a list. Prompts user to search something else after a cool-down period.
    KeyError
        Raised when the script cannot find a keyword in the html. excepts to either writing "none"
        in results or prompts you to search again
    AttributeError
        An attribute doesnt exist. Raised when code cant find an attribute in the html. Skips over
        said html and writes "none" in the CSV file. Continues the scraper onto the next item in list.
    PermissionError
        Caused when the CSV file trying to be write is open. Prompts user to close said file and
        restart code

    Notes
    -----
    Script will not work in some external programs where web-scraping is against terms and conditions for example, repl.it.
    """
    while True:
        # running user input loop
        # saving input_code() into a list
        # splitting the user_input into two variables
        user_input = input_code()
        user_url = user_input[0]
        user_search = user_input[1]

        # URl to web scrap from.
        # LINK is a constant
        # Default URL search link + users search input
        url = constants.LINK + user_url

        # opens the connection and downloads html page from url
        uClient = url_req(url)

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        # putting it inside a variable to prevent the whole code crashing
        page_html = uClient.read()
        uClient.close()

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        page_soup = soup(page_html, "html.parser")

        # finds all of the containers on neweggs html doc
        # Grabs each product on the page
        containers = page_soup.findAll("div", {"class": "item-container"})

        # creating a loop that detects containers
        try:
            # creating variable container so I can loop through the containers within neweggs html file
            # exiting the list if variable is made
            container = containers[0]
            break

        # If can't find any containers two errors occur as a list cannot be created and then as a specific word cant be found
        # No search results creates said errors
        # Sending the user back to input
        except (ValueError, IndexError):
            print("I'm sorry. There are no search results for '" + user_search + "'. \nPlease wait 10 seconds before searching again to prevent excessive traffic")
            # timer counting down from 10seconds before restarting the input loop
            timer(11)
            continue

    # try/ except function detecting whether or not the CSV file is currently in use
    try:
        # the CSV files name
        # opening the CSV file allowing us to write
        file_name = "products.csv"
        file = open(file_name, "w")

        # if CSV file is open show print statement
    except PermissionError:
        print("Please close the CSV file and then run the program again.")

        # stopping the program
        sys.exit()

    # naming the headers to write to the CSV file
    headers = "Brand, Product name, Price, Original price, Rating, Additional promotions\n"

    # writing the headers to the CSV file
    file.write(headers)

    # creating the loop
    # loop adds to container[] list as it goes through all of the containers on the webpage
    # once all containers in neweggs html file have been recorded the loop will break
    for container in containers:

        # try/ except command used to allow the code to skip over any missing index's (IndexError), or words (KeyError) in neweggs html file
        try:
            rating_container = container.findAll("a", {"class": "item-rating"})
            rating = str(rating_container[0]["title"])
            rating = [int(s) for s in rating.split() if s.isdigit()]
        except (IndexError, KeyError):

            # if there isn't a word in neweggs html file, specifically title under the dictated directory - skips rating
            # if there isn't an index that is in reach or rating on a product, writing 'none' in the ratings place
            # writing 'none' in the ratings place
            rating = "none"

        # try/ except command used to allow the code to skip over any missing index's in neweggs html file
        try:
            # scraping newegg.com for a products original price
            origin_price_container = container.findAll("li", {"class": "price-was"})
            origin_price = origin_price_container[0].text
        except IndexError:

            # if there isn't an index that is in reach or original price on a product, writing 'none' in the original price's place
            origin_price = "none"

        # try/ except command used to allow the code to skip over any missing words in neweggs html file
        try:
            # scraping newegg.com for a products price
            model = container.img["alt"]
        except KeyError:

            # if there isn't a word in neweggs html file, specifically alt under the dictated directory - skips model
            # writing 'none' in the models place
            model = "none"

        # try/ except command used to allow the code to skip over any missing index's in neweggs html file
        try:
            # scraping newegg.com for a products price
            price_container = container.findAll("li", {"class": "price-current"})
            price = price_container[0].text
        except IndexError:

            # if there isn't an index that is in reach or price on a product, writing 'none' in the price's place
            price = "none"

        # try/ except command used to allow the code to skip over any missing index's in neweggs html file
        try:
            # scraping newegg.com for a products brand name
            brand_container = container.findAll("a", {"class": "item-brand"})
            brand = brand_container[0].img["alt"]
        except IndexError:

            # if there isn't an attribute or rating on a product, writing 'none' in the brands place
            brand = "none"

        # try/ except command used to allow the code to skip over any missing attributes in neweggs html file
        try:
            # scraping newegg.com for a products rating out of 5
            promotion = container.div.p.text
        except AttributeError:

            # if there isn't an attribute or promotion on a product, writing 'none' in the ratings place
            promotion = "none"

        # writing the results of the web-scraper to the CSV file, as it loops around until it reaches the bottom of the list/ last container on the page
        file.write(str(brand) + "," + str(model.replace(",", "|")) + "," + str(price) + "$USD," + str(origin_price) + "$USD," + str(rating) + "/[5]," + str(promotion.replace(",", "-")) + "\n")

    # closing the CSV file to allow user to open it
    file.close()
    return [file_name]


def run():
    """
    Def to run the program.
    """
    # running function introduction
    introduction()

    # running function web_scraper
    # retrieving filename
    filename = web_scraper()

    print("Search finished! Thank you for using the newegg.com web-scraper. \nYour results have been written to a CSV file! \nYour CSV file is called " + str(filename) + "! Your file directory is: \n" + os.getcwd() + "\\products.csv")


web_scraper()