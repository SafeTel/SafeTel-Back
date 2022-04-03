##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DBClean
##

# INFRA
# Client mongo db import
import pymongo

from typing import Tuple

from MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

class DBClean(MongoDBWorker):
    def __init__(self, client, db):
        super().__init__(db)
        self.MongoDBClient = client
        self.DBAndCollectionPair = []

    def setDatabasesCollectionPair(self, db: str, collections):
        self.DBAndCollectionPair.append(Tuple(db, collections))

    def run(self):
        print('I"m working')
