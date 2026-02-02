import os
from pymongo import MongoClient

def get_mongo_client():
    uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    return MongoClient(uri)

def log_to_mongo(collection, data):
    client = get_mongo_client()
    db = client["carbon_tracker"]
    db[collection].insert_one(data)
