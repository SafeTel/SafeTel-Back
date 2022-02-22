##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## WhiteListDB
##

# Client mongo db import
import pymongo

# MongoDBMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

# Melchior Internal Utils
from Infrastructure.Services.MongoDB.Melchior.UserLists.UserListsWorker import UserListsWorker
import os

# Object to represent table Whitelist
class WhitelistDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Whitelist = self.db['Whitelist']
        self.DBWatcher = MongoDBWatcher(self.Whitelist)
        self.DBWorker = MongoDBWorker(self.Whitelist)
        self.ULWorker = UserListsWorker(self.Whitelist)


    def newWhitelist(self, guid):
        data = {
            "guid": guid,
            "PhoneNumbers": []
        }
        self.DBWorker.InsertDocument(data)


    def deleteWhitelist(self, guid):
        self.DBWorker.DeleteDocument({'guid': guid})


    def exists(self, guid):
        return self.DBWatcher.IsDocument("guid", guid)


    def getWhitelistForUser(self, guid):
        return self.DBWatcher.GetDocument("guid", guid)


    def addWhitelistNumberForUser(self, guid, number):
        self.ULWorker.AddNumberFromList(guid, number)


    def delWhitelistNumberForUser(self, guid, number):
        self.ULWorker.DeleteNumberFromList(guid, number)
