import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = "ResearchAgent"

    @staticmethod
    def get_mongo_client():
        if not Settings.MONGODB_URI:
            raise ValueError("MONGODB_URI is not set in the environment variables")
        client = MongoClient(Settings.MONGODB_URI)
        return client[Settings.DB_NAME]

settings = Settings()