from src.database.mongodb import MongodbOperation

if __name__ == "__main__":

    t = MongodbOperation()
    t.insert_many("collect", [1,2,3,4])
