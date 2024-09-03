from pymongo import MongoClient
from config import MONGO_URI
from pymongo.server_api import ServerApi

db = None

def get_db():
    """
    Establishes a connection to the MongoDB cluster and returns the database instance.
    Returns:
        db (Database): The MongoDB database instance.
    """
    global db
    if db is None:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'), connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
        db = client["spotify_data"]
    return db