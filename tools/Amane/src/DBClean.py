##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DBClean
##


### LOGIC
# env var import
import os

# INFRA
# Client mongo db import
from typing import Any

class DBClean():
    def __init__(self, client):
        self.__MongoDBClient = client
        self.__DBAndCollectionPair = []

        # All DB on mongoDB
        self.__DB = {
            os.getenv("DB_MELCHIOR"):  self.__MongoDBClient[os.getenv("DB_MELCHIOR")],
            os.getenv("DB_CASPER"):    self.__MongoDBClient[os.getenv("DB_CASPER")],
            os.getenv("DB_CASPER_02"): self.__MongoDBClient[os.getenv("DB_CASPER_02")],
            os.getenv("DB_BALTHASAR"): self.__MongoDBClient[os.getenv("DB_BALTHASAR")]
        }

    # Set a pair of database and collection to clean
    # The pair is store as tuple in the format:
    #
    #   (DBName, ['Collection_1', 'Collection_2', 'Collection_3'])
    #
    def setDatabasesCollectionPair(self, db: str, collections):
        self.__DBAndCollectionPair.append((db, collections))

    # Parse __DBAndCollectionPair array to perform deletion on every collections
    def run(self):
        for MongoConfig in self.__DBAndCollectionPair:

            if MongoConfig == None:
                raise Exception("MongoConfig tuple None")

            DBName = MongoConfig[0]
            if DBName == None:
                raise Exception("DBName None")
            elif self.__DB[DBName] == None:
                raise Exception("DB don't exist")

            for CollectionName in MongoConfig[1]:
                if CollectionName == None:
                    raise Exception("Collection name None")
                # Get the collection from DB
                self.MongoDB = self.__DB[DBName][CollectionName]
                self.DeleteManyDocument(self.MongoDB, {})

    # Delete multiple documents
    def DeleteManyDocument(self, db, query: Any):
        if query == None:
            return
        db.delete_many(query)
