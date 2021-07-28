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

# Not found definition
NOT_FOUND = 404

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
        self.History.insert_one(data)

    def deleteHistory(self, guid):
        self.History.delete_one({'guid': guid})

    def exists(self, guid):
        result = self.History.find_one({'guid': guid})
        return True if result is not None else False

    def getHistoryForUser(self, id):
        query = {
            'userId': str(id)
        }
        result = self.History.find_one(query)
        if result is None:
            return NOT_FOUND
        return result

    def delHistoryCallForUser(self, id, number, timestamp):
        query = {
            'userId': str(id)
        }
        result = self.History.find_one(query)
        if result is None:
            return
        updated_values = result["history"]
        for i in range(len(updated_values)):
            if updated_values[i]['number'] == number and updated_values[i]['time'] == str(timestamp):
                del updated_values[i]
                break
        print(updated_values)
        query_values = { "$set": { 'history': updated_values } }
        self.History.update_one(query, query_values)
