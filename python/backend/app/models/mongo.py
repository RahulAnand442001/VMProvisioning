from pymongo.mongo_client import MongoClient
from controllers.db import get_secret
from bson import ObjectId


class MongoDB:
    DB = "vmpoc"
    COLLECTION = "deployments"

    def __init__(self):
        MDB_SECRET = get_secret("VMDeploy/mongodb")
        USERNAME = MDB_SECRET["MDB_USER"]
        PASS = MDB_SECRET["MDB_PASS"]
        MONGODB_URL = MDB_SECRET["MDB_URL"]
        self.client = MongoClient(f"mongodb://{USERNAME}:{PASS}@{MONGODB_URL}/")

    def insertDocument(self, document):
        result = self.client[self.DB][self.COLLECTION].insert_one(document)
        return str(result.inserted_id)

    def insertManyDocuments(self, documents):
        result = self.client[self.DB][self.COLLECTION].insert_many(documents)
        return result.inserted_ids

    def getAllDocuments(self, projection):
        result = self.client[self.DB][self.COLLECTION].find({}, projection)
        return list(result)

    def getDocument(self, query):
        result = self.client[self.DB][self.COLLECTION].find_one(query)
        return result

    def updateDocument(self, id, result):
        query = {"_id": ObjectId(id)}
        result = self.client[self.DB][self.COLLECTION].update_one(
            query, {"$set": {"status": result}}
        )
