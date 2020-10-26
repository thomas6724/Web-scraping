from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup

graphics_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics+cards'

# opens the connection and downloads html page from url
uClient = url_req(graphics_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
# putting it inside a variable to prevent the whole code crashing
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# Grabs each product
containers = page_soup.findAll("div", {"class": "item-container"})

# prototyping a for loop that basically goes through the page as I will do something like "for every container in containers
contain = containers[0]
container = containers[0]
print(container.findAll("a", {"class": "item-rating"}))

# creating the loop
for container in containers:
    brand = container.div.div.a.img["title"]

    try:
        promotion = container.div.p.text
    except Exception:
        promotion = "none"

    price_container = container.findAll("li", {"class": "price-current"})
    price = price_container[0].text

    model = container.a.img["alt"]

    # print(brand)
    # print(price)
    # print(model)
    # print(promotion)