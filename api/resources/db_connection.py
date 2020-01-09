import pymongo

myclient = pymongo.MongoClient("mongodb://klopsiu:demo1234@mongodb:27017/xkom")
db = myclient["xkom"]
collection = db["Smartphones"]
