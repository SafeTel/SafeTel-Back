##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BlackListDB
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker
# Melchior Internal Utils
from Infrastructure.Services.MongoDB.Melchior.UserLists.UserListsWorker import UserListsWorker

### LOGIC
# Get env vars import
import os

# Object to represent table Blacklist
class BlacklistDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Blacklist = self.db['Blacklist']
        self.DBWatcher = MongoDBWatcher(self.Blacklist)
        self.DBWorker = MongoDBWorker(self.Blacklist)
        self.ULWorker = UserListsWorker(self.Blacklist)


    def newBlacklist(self, guid: str):
        NewBlacklistDocument = {
            "guid": guid,
            "PhoneNumbers": []
        }
        self.DBWorker.InsertDocument(NewBlacklistDocument)


    def deleteBlacklist(self, guid: str):
        self.DBWorker.DeleteDocument(guid)


    def exists(self, guid: str):
        return self.DBWatcher.IsDocument("guid", guid)


    def getBlacklistForUser(self, guid: str):
        return self.DBWatcher.GetDocument("guid", guid)


    def GetBlacklistNumbers(self, guid: str):
        return self.DBWatcher.GetDocument("guid", guid)["PhoneNumbers"]


    def addBlacklistNumberForUser(self, guid: str, number: str):
        self.ULWorker.AddNumberFromList(guid, number)


    def delBlacklistNumberForUser(self, guid: str, number: str):
        self.ULWorker.DeleteNumberFromList(guid, number)
