##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## HistoryDB
##

# Client mongo db import
import pymongo

# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker


import os

# Object to represent table History
class HistoryDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.History = self.db['History']
        self.DBWatcher = MongoDBWatcher(self.History)
        self.DBWorker = MongoDBWorker(self.ApiKeyLog)

    def newHistory(self, guid):
        data = {
            "guid": guid,
            "History": []
        }
        self.DBWorker.InsertDocument(self.History, data)

    def deleteHistory(self, guid):
        self.DBWorker.DeleteDocument(self.History, {'guid': guid})

    def exists(self, guid):
        return self.DBWatcher.IsDocument("guid", guid)

    def getHistoryForUser(self, guid):
        return self.DBWatcher.GetDocument("guid", guid)

    def delHistoryCallForUser(self, guid, number, timestamp):
        query = {
            'guid': str(guid)
        }
        result = self.DBWatcher.GetDocument("guid", guid)
        if result is None:
            return
        updated_values = result["History"]
        for i in range(len(updated_values)):
            if updated_values[i]['number'] == number and updated_values[i]['time'] == timestamp:
                del updated_values[i]
                break
        query_values = { "$set": { 'History': updated_values } }
        self.History.update_one(query, query_values)

    def addHistoryCallForUser(self, guid, number, origin, time):
        query = {
            'guid': str(guid)
        }
        result = self.DBWatcher.GetDocument("guid", guid)
        if result is None:
            return

        import sys

        updated_values = result["History"]
        print(updated_values, file=sys.stderr)
        updated_values.append({
                "number": number,
                "origin": origin,
                "time": time
            }
        )
        print(updated_values, file=sys.stderr)
        query_values = { "$set": { 'History': updated_values } }
        self.History.update_one(query, query_values)
