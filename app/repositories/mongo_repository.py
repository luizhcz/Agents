from pymongo import MongoClient
from app.core.config import settings
from bson import ObjectId

class MongoRepository:
    def __init__(self):
        self.collection = settings.get_mongo_client()['results']

    def save_result(self, result_data: dict):
        try:
            # Se o dicionário tiver um campo 'id', converte-o para ObjectId
            if "id" in result_data:
                result_data["_id"] = result_data["id"]  # Converte o campo 'id' em ObjectId
                del result_data["id"]  # Remove o campo 'id' original, se preferir usar '_id'

            self.collection.insert_one(result_data)
            print(f"Result saved successfully with _id: {result_data['_id']}")
        except Exception as e:
            print(f"Failed to save result: {e}")

    def find_result_by_id(self, result_id: str):
        try:
            # Verifica se o result_id é um ObjectId válido, se estiver usando o campo _id do MongoDB
            return self.collection.find_one({"_id": ObjectId(result_id)})
        except Exception as e:
            print(f"Error fetching result by ID: {e}")
            return None
