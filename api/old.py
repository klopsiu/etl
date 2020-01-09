# https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html?page=2

import pymongo
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Extract data

number_of_products = 0
index = 0
html_list = list(range(200)) # Maximum number of pages.
# Loop all pages where are products. Loop ends when returns empty list.
while True:
    url = 'https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html?page={}'.format(index)
    #website = urlopen(url)
    website = requests.get(url)
    f = open("cache/page_{}.txt".format(index), "w+")
    f.write(str(website.content))
    f.close()
    soup = BeautifulSoup(website.content)
    html_list[index] = soup.findAll("div", {"class": "sc-4el5v8-13 goPzRd"})
    if len(html_list[index]) < 1:
        break
    # Save every result set to the file
    number_of_products += len(html_list[index])
    index += 1

result = list(range(number_of_products))
# Transform every product
wasted_place = 0   # number of used boxes in result list.
for page in html_list:
    if wasted_place >= number_of_products:
        break
    for one in page:
        title = one.find("h3")
        # Searching every rate and parse it.
        rate = one.find("a", {"class": "sc-4el5v8-16 kIMsrT sc-1u6l9jk-1 ixvhfp sc-673ayz-0 dfQSis"})
        if rate is None:
            number_of_products -= 1
            continue
        converted_rate = re.findall(r'[-][\s]([\w|,]*)', rate.get("title"))
        if len(converted_rate) < 1:
            converted_rate = [0]
        # Split data from ul tag
        data = one.find("ul", {"class": "sc-1vco2i8-0 sc-4el5v8-15 fLNKyj sc-1vco2i8-1 ZosGi"})
        if data is None:
            number_of_products -= 1
            continue
        r = re.findall(r'[:]\s([(\w|\s|\.)]*)', str(data.get("title")))
        # Checking for all elements, if something is wrong, then left this product.
        if len(r) != 4:
            number_of_products -= 1

        # Save data to object.
        else:
            result[wasted_place] = {"Tytuł": title.get('title', "No title"),
                          "Średnia ocena": converted_rate[0],
                          "Ekran": r[0],
                          "Procesor": r[1],
                          "Pamięc": r[2],
                          "System": r[3]}
            wasted_place += 1

for one in result:
    print(one)

'''
for tag in all:
    tdTags = tag.find_all("div")
    for next in tdTags:
        print(next.text)
'''
myclient = pymongo.MongoClient("mongodb://klopsiu:demo1234@mongodb:27017/allegro")
