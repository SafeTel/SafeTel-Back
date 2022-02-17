##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## BlackListDB
##

# Client mongo db import
import pymongo

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument, IsDocument
from DataBases.InternalUtils.DataWorker import InsertDocument, DeleteDocument

# Melchior Internal Utils
from DataBases.Melchior.InternalUtils.DataWorker import AddNumberToPhoneList, DeleteNumberFromPhoneList

import os

# Object to represent table Blacklist
class BlacklistDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Blacklist = self.db['Blacklist']

    def newBlacklist(self, guid):
        data = {
            "guid": guid,
            "PhoneNumbers": []
        }
        InsertDocument(self.Blacklist, data)

    def deleteBlacklist(self, guid):
        DeleteDocument(self.Blacklist, {'guid': guid})

    def exists(self, guid):
        return IsDocument(self.Blacklist, "guid", guid)

    def getBlacklistForUser(self, guid):
        return GetDocument(self.Blacklist, "guid", guid)

    def addBlacklistNumberForUser(self, guid, number):
        AddNumberToPhoneList(self.Blacklist, guid, number)

    def delBlacklistNumberForUser(self, guid, number):
        DeleteNumberFromPhoneList(self.Blacklist, guid, number)
