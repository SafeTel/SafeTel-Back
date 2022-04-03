##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DBClean
##

# INFRA
# Client mongo db import
from datetime import datetime
import pymongo

# Logs importes
import logging

from MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

class DBClean(MongoDBWorker):
    def __init__(self, client, db = None):
        super().__init__(db)
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
        self.__MongoDBClient = client
        self.__DBAndCollectionPair = []

    # Set a pair of database and collection to clean
    # The pair is store as tuple in the format:
    #
    #   (DBName, ['Collection_1', 'Collection_2', 'Collection_3'])
    #
    def setDatabasesCollectionPair(self, db: str, collections):
        self.__DBAndCollectionPair.append((db, collections))

    # Parse __DBAndCollectionPair array to perform deletion on every collections
    def run(self):
        logging.info('Start - Database cleaning')

        for MongoConfig in self.__DBAndCollectionPair:
            if MongoConfig == None:
                raise Exception("MongoConfig tuple None")
            DBName = MongoConfig[0]
            if DBName == None:
                raise Exception("DBName None")
            DB = self.__MongoDBClient[DBName]
            for Collection in MongoConfig[1]:
                if Collection == None:
                    raise Exception("Collection name None")
                self.MongoDB = DB[Collection]
                self.DeleteManyDocument({})
        logging.info('End - Database cleaning')
