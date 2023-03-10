import os
import pymongo
import certifi

ca = certifi()


class MongodbOperation:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB_KEY"), tlsCAFile=ca)
        self.db_name = "sensorDB"

        print(self.client)

    def insert_many(self, collection_name, records: list):
        self.client[self.db_name][collection_name].insert_many(records)

    def insert(self, collection_name, record):
        self.client[self.db_name][collection_name].insert_one(record)


