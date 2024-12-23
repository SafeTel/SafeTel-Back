##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DataWorker
##

# INFRA
# Client mongo db import
import pymongo

class MongoDBWorker():
    def __init__(self, db):
        self.NOT_FOUND = 404
        self.MongoDB = db


    # Create a document linked in MongoDb
    def InsertDocument(self, data):
        if data == None:
            return
        self.MongoDB.insert_one(data)


    # Delete a document linked to a guid in MongoDb
    def DeleteDocument(self, guid: str):
        if guid == None:
            return
        self.MongoDB.delete_one({"guid": guid})


    # Delete a document linked to a prop in MongoDb
    def DeleteDocumentByProp(self, prop: str, guid: str):
        if guid == None:
            return
        self.MongoDB.delete_one({prop: guid})
