import pymongo

class MongoDBHelper:
    def __init__(self, collection = 'owner'):
        uri = "mongodb+srv://vikuu2204:vikas123@cluster0.wumoqgr.mongodb.net/?retryWrites=true&w=majority"

        client = pymongo.MongoClient(uri)
        self.db = client['vikas_kumar']
        self.collection = self.db[collection]
        print("MongoDB Connected")

    def insert(self, document):
        result = self.collection.insert_one(document)
        print("Document Inserted:", result)

        return result

    def delete(self, query):
        result = self.collection.delete_one(query)
        print("Document Deleted:", result)

    def fetch(self, query=""):
        documents = self.collection.find(query)  # find_one()
        return list(documents)

    def update(self, document, query):
        update_query = {'$set': document}
        result = self.collection.update_one(query, update_query)
        print("Updated Document:", result.modified_count)




