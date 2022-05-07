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

### LOGIC
# env var import
import os

class DBClean(MongoDBWorker):
    def __init__(self, client, db = None):
        super().__init__(db)
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
        self.__MongoDBClient = client
        self.__DBAndCollectionPair = []

        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__BalthasarName = os.getenv("DB_BALTHASAR")

        # All DB on mongoDB
        self.__DB = {
            self.__MelchiorName:  self.__MongoDBClient[self.__MelchiorName],
            self.__CasperName:    self.__MongoDBClient[self.__CasperName],
            self.__CasperTwoName: self.__MongoDBClient[self.__CasperTwoName],
            self.__BalthasarName: self.__MongoDBClient[self.__BalthasarName]
        }

        # All collections on mongoDB
        self.__Collections = {
            'Blacklist':        self.__DB[self.__MelchiorName]['Blacklist'],
            'History':          self.__DB[self.__MelchiorName]['History'],
            'User':             self.__DB[self.__MelchiorName]['User'],
            'Whitelist':        self.__DB[self.__MelchiorName]['Whitelist'],
            'ApiKeyLog':        self.__DB[self.__CasperName]['ApiKeyLog'],
            'Contributors':     self.__DB[self.__CasperName]['Contributors'],
            'GoogleServices':   self.__DB[self.__CasperTwoName]['GoogleServices'],
            'Boxes':            self.__DB[self.__BalthasarName]['Boxes'],
            'UnclaimedBoxes':   self.__DB[self.__BalthasarName]['UnclaimedBoxes'],
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
        logging.info('Start - Database cleaning')

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
                self.MongoDB = self.__Collections[CollectionName]
                self.DeleteManyDocument({})
        logging.info('End - Database cleaning')
