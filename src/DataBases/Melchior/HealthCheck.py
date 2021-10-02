##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Heakth Check
##

# Client mongo db import
import pymongo

# Import db name
from config import dbname


# Object to represent table History
class HistoryDB():
    def __init__(self, db_name=dbname):
        print("__init__")
        # self.client = pymongo.MongoClient(URI_MELCHIOR)
        # self.db = self.client[db_name]
        # self.History = self.db['History']

    # def newHistory(self, guid):
    #     data = {
    #         "guid": guid,
    #         "History": []
    #     }
    #     InsertDocument(self.History, data)

    # def deleteHistory(self, guid):
    #     DeleteDocument(self.History, {'guid': guid})

    # def exists(self, guid):
    #     return IsDocument(self.History, "guid", guid)

    # def getHistoryForUser(self, guid):
    #     return GetDocument(self.History, "guid", guid)

    # def delHistoryCallForUser(self, guid, number, timestamp):
    #     result = GetDocument(self.History, "guid", guid)
    #     if result is None:
    #         return
    #     updated_values = result["History"]
    #     for i in range(len(updated_values)):
    #         if updated_values[i]['number'] == number and updated_values[i]['time'] == str(timestamp):
    #             del updated_values[i]
    #             break
    #     query_values = { "$set": { 'history': updated_values } }
    #     self.History.update_one(query, query_values)
