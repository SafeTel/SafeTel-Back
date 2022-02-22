##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DataWatcher
##

### INFRA
# Client mongo db import
import pymongo

class MongoDBWatcher():
    def __init__(self, db):
        self.NOT_FOUND = 404
        self.MongoDB = db


    # Look for a document by giving the db, a query, and data to compare
    def GetDocument(self, query, data):
        query_mongo = {
            query: data
        }
        result = self.MongoDB.find_one(query_mongo)
        return result


    # Look for a document by giving the db, a query, and data to compare
    def IsDocument(self, query, data):
        query_mongo = {
            query: data
        }
        result = self.MongoDB.find_one(query_mongo)
        return True if result is not None else False
