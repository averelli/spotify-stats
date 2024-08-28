from pymongo import MongoClient
from config import MONGO_URI

db = None

def get_db():
    """
    Establishes a connection to the MongoDB cluster and returns the database instance.
    Returns:
        db (Database): The MongoDB database instance.
    """
    global db
    if db is None:
        client = MongoClient(MONGO_URI)
        db = client["spotify_data"]
    return db