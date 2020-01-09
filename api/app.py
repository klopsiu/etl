# https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html?page=2
# POST/PUT: docker exec python_projekt curl -d "param1=value1&param2=value2" -X POST http://localhost:5000/etl
# GET curl -v http://localhost:5000/etl

from flask import Flask
from flask_restful import Api
from resources.extract import Extract
from resources.transform import Transform
from resources.load import Load
from resources.database_data import DatabaseData

app = Flask(__name__)
api = Api(app, prefix="/api")

api.add_resource(Extract, '/extract')
api.add_resource(Transform, '/transform')
api.add_resource(Load, '/load')
api.add_resource(DatabaseData, '/data')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')


