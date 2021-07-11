##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Melchior
##

# Client mongo db import
import pymongo

# Import db settings connextion
from config import client, password, dbname

# URI to connect to our Atlas DB
URI_MONGO_ATLAS = 'mongodb+srv://' + client + ':' + password + '@safetel-back-cluster.klq5k.mongodb.net/' + dbname + '?retryWrites=true&w=majority'

# Not found definition
NOT_FOUND = 404

# Object to represent table User
class UserDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MONGO_ATLAS)
        self.db = self.client[db_name]
        self.Users = self.db['User']

# Object to represent table Blacklist
class BlacklistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MONGO_ATLAS)
        self.db = self.client[db_name]
        self.Blacklist = self.db['Blacklist']

    def getBlacklistForUser(self, id):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return NOT_FOUND
        return result

    def addBlacklistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.append(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Blacklist.update_one(query, query_values)

    def delBlacklistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.remove(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Blacklist.update_one(query, query_values)

# Object to represent table Whitelist
class WhitelistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MONGO_ATLAS)
        self.db = self.client[db_name]
        self.Whitelist = self.db['Whitelist']

    def getWhitelistForUser(self, id):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return NOT_FOUND
        return result

    def addWhitelistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.append(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Whitelist.update_one(query, query_values)

    def delWhitelistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.remove(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Whitelist.update_one(query, query_values)

# Object to represent table History
class HistoryDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MONGO_ATLAS)
        self.db = self.client[db_name]
        self.History = self.db['History']

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
