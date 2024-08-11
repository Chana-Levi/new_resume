from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='my_resume'):
        self.client = MongoClient(uri)
        self.db_name = db_name
        self.db = self.client[db_name]
        self.ensure_collections(['jobs', 'organizations', 'matches', 'candidates', 'resumes'])

    def get_database(self):
        return self.db

    def ensure_collections(self, collections):
        for collection_name in collections:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                print(f"Collection '{collection_name}' created in database '{self.db_name}'")
            else:
                print(f"Collection '{collection_name}' already exists in database '{self.db_name}'")


db_connection = MongoDB().get_database()