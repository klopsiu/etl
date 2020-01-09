from flask_restful import Resource, Api
from .db_connection import collection

class DatabaseData(Resource):
    # Fetch data
    def get(self):
        try:
            data = list(collection.find({}, {"_id":0}))
        except Exception:
            return "Db error", 400
        return data, 200

    # Clean data
    def delete(self):
        try:
            collection.remove({})
        except Exception:
            return "Db error", 400

        return "Database has been cleaned", 200
