##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## HistoryDB
##

# Client mongo db import
import pymongo

# Import db name
from config import dbname

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument, IsDocument
from DataBases.InternalUtils.DataWorker import InsertDocument, DeleteDocument

# Object to represent table History
class HistoryDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.History = self.db['History']

    def newHistory(self, guid):
        data = {
            "guid": guid,
            "History": []
        }
        InsertDocument(self.History, data)

    def deleteHistory(self, guid):
        DeleteDocument(self.History, {'guid': guid})

    def exists(self, guid):
        return IsDocument(self.History, "guid", guid)

    def getHistoryForUser(self, guid):
        return GetDocument(self.History, "guid", guid)

    def delHistoryCallForUser(self, guid, number, timestamp):
        query = {
            'guid': str(guid)
        }
        result = GetDocument(self.History, "guid", guid)
        if result is None:
            return
        updated_values = result["History"]
        for i in range(len(updated_values)):
            if updated_values[i]['number'] == number and updated_values[i]['time'] == timestamp:
                del updated_values[i]
                break
        query_values = { "$set": { 'History': updated_values } }
        self.History.update_one(query, query_values)
