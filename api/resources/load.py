from flask_restful import Resource, Api
import pymongo
import json
import os
from .db_connection import collection

class Load(Resource):

    def get(self):
        # TO LOAD JSON from data.json
        try:
            with open('cache/data.json', 'r') as fp:
                data = list(json.load(fp))
        except FileNotFoundError:
            return "You need to Extract and Transform data first", 400

        try:
            database_content = list(collection.find({}))
        except Exception:
            return "Db error", 400

        data_save = []
        flag = 2

        if isinstance(database_content, list):
            for new_document in data:
                flag = 1
                for document in database_content:
                    if new_document["Tytuł"] == document["Tytuł"]:
                        flag = 0
                        break
                if flag == 1:
                    # raise Exception(new_document)
                    data_save.append(new_document)

        number_of_elements = len(database_content)+len(data_save)

        if len(data_save) > 0:
            try:
                result = collection.insert_many(data_save)
            except Exception:
                return "Db error", 400

        os.remove('cache/data.json')

        return "Data has been loaded, in database is {} elements".format(number_of_elements), 200