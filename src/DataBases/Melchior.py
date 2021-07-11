##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Melchior
##

import pymongo
from config import client, password, dbname

### 3.6 or later ###
URI_MONGO_ATLAS = 'mongodb+srv://' + client + ':' + password + '@safetel-back-cluster.klq5k.mongodb.net/' + dbname + '?retryWrites=true&w=majority'

NOT_FOUND = 404

class UserDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MONGO_ATLAS)
        self.db = self.client[db_name]
        self.Users = self.db['User']

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
