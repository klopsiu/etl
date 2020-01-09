from flask_restful import Resource, Api
import requests

class Extract(Resource):

    # Extract data
    def get(self, total = 30):
        index = 0
        while True:
            if index >= total:
                break
            url = 'https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html?page={}'.format(index)
            # website = urlopen(url)
            website = requests.get(url)
            with open("cache/page_{}.txt".format(index), "w+") as f:
                f.write(str(website.content))
                f.close()
            index += 1
        with open("cache/index.txt", "w+") as f:
            f.write('%d' % index)
        return "Data has been extracted, downloaded {} files".format(index), 200
