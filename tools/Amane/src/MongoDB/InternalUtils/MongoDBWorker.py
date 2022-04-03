##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DataWorker
##

# INFRA
# Client mongo db import
from typing import Any
import pymongo

class MongoDBWorker():
    def __init__(self, db = None):
        self.MongoDB = db
    
    def setMongoDB(self, db):
        self.MongoDB = db

    # Delete multiple documents
    def DeleteManyDocument(self, query: Any):
        if query == None:
            return
        self.MongoDB.delete_many(query)
