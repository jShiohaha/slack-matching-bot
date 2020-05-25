import os
from datetime import datetime

# external package imports
import pymongo


class PyMongoClient:
    hostname = os.getenv('PYMONGO_HOSTNAME')
    username = os.getenv('PYMONGO_USERNAME')
    password = os.getenv('PYMONGO_PASSWORD')

    def __init__(self):
        self.mongoDbUrl = ("mongodb+srv://{}:{}@{}/test?"
                           "retryWrites=true&w=majority").format(self.username,
                                                              self.password,
                                                              self.hostname)
        self.client = pymongo.MongoClient(self.mongoDbUrl, port=27017)
        self.database = None
        self.collection = None

    def _getClient(self):
        return self.client

    def _getDatabase(self):
        return self.database

    def _setDatabase(self, database):
        self.database = self._getClient()[database]

    def _getCollection(self):
        return self.collection

    def _setCollection(self, collection):
        self.collection = self._getDatabase()[collection]


class GraphMongoClient(PyMongoClient):
    databaseName = os.getenv('PYMONGO_DB_NAME')
    collectionName = os.getenv('PYMONGO_GRAPH_COLLECTION')

    def __init__(self):
        super().__init__()
        self._setDatabase(self.databaseName)
        self._setCollection(self.collectionName)

    def insert_graph_instance(self, graph, date=None):
        if date is None:
            date = datetime.now()
        item = {
            'date': date,
            'graph': graph
        }
        self._getCollection().insert_one(item)

    def get_latest_graph_instance(self):
        result = self._getCollection().find().sort('date', pymongo.DESCENDING).limit(1)
        res_as_list = list(result)
        return None if len(res_as_list) == 0 else res_as_list[0]
