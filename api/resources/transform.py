from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import re
import json
import os
from glob import glob

class Transform(Resource):

    def get(self):
        try:
            with open("cache/index.txt", "r+") as index_file:
                index = index_file.read()
        except FileNotFoundError:
            return "To transform data, first you need to extract it", 400

        number_of_products = 0
        html_list = list(range(200))  # Maximum number of pages - static list, necessary to void inefficient expressions.

        for i in range(int(index)):
            f = open("cache/page_{}.txt".format(i), "r+")
            website = f.read()
            soup = BeautifulSoup(website)
            #html_list[i] = soup.findAll("div", {"class": "sc-4el5v8-13 goPzRd"})
            html_list[i] = soup.findAll("div", {"class": "sc-1yu46qn-7 cRrTHy sc-2ride2-0 eYsBmG"})
            if len(html_list[i]) < 1:
                break
            # Save every result set to the file
            number_of_products += len(html_list[i])

        result = list(range(number_of_products))
        # Transform every product
        wasted_place = 0  # number of used boxes in result list.
        for page in html_list:
            if wasted_place >= number_of_products:
                break
            for one in page:
                title = one.find("h3")
                # Searching every rate and parse it.
                #rate = one.find("a", {"class": "sc-4el5v8-16 kIMsrT sc-1u6l9jk-1 ixvhfp sc-673ayz-0 dfQSis"})
                rate = one.find("a", {"class": "sc-1yu46qn-16 tGJLo sc-1ngc1lj-1 eQvjal sc-4ttund-0 kWNYsq"})
                if rate is None:
                    number_of_products -= 1
                    continue
                converted_rate = re.findall(r'[-][\s]([\w|,]*)', rate.get("title"))
                if len(converted_rate) < 1:
                    converted_rate = [0]
                # Split data from ul tag
                #data = one.find("ul", {"class": "sc-1vco2i8-0 sc-4el5v8-15 fLNKyj sc-1vco2i8-1 ZosGi"})
                data = one.find("ul", {"class": "vb9gxz-0 sc-1yu46qn-15 bhmXit vb9gxz-1 iNfAAG"})
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

        cleaned_result = [d for d in result if isinstance(d, dict)]

        # Remove downloaded duplicates
        cleaned = [dict(t) for t in {tuple(d.items()) for d in cleaned_result}]

        with open('cache/data.json', 'w') as fp:
            json.dump(cleaned, fp, indent=4)
        # Cleaning files from extracting
        for file in glob('cache/page*'):
            os.remove(file)
        os.remove('cache/index.txt')

        return cleaned, 200