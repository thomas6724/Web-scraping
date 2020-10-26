import time


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

user_search = input_code()
print(user_search[0])