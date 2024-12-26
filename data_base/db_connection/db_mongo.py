#connect to mongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/new_api')
db = client['new_api']
collection = db['events']


#connect to csv