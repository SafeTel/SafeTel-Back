##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## WhiteListDB
##

# Client mongo db import
import pymongo

# Import db name and db URI
from config import dbname, URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument, IsDocument
from DataBases.InternalUtils.DataWorker import InsertDocument, DeleteDocument

# Melchior Internal Utils
from DataBases.Melchior.InternalUtils.DataWorker import AddNumberToPhoneList, DeleteNumberFromPhoneList

# Object to represent table Whitelist
class WhitelistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Whitelist = self.db['Whitelist']

    def newWhitelist(self, guid):
        data = {
            "guid": guid,
            "PhoneNumbers": []
        }
        InsertDocument(self.Whitelist, data)

    def deleteWhitelist(self, guid):
        DeleteDocument(self.Whitelist, {'guid': guid})

    def exists(self, guid):
        return IsDocument(self.Whitelist, "guid", guid)

    def getWhitelistForUser(self, guid):
        return GetDocument(self.Whitelist, "guid", guid)

    def addWhitelistNumberForUser(self, guid, number):
        AddNumberToPhoneList(self.Whitelist, guid, number)

    def delWhitelistNumberForUser(self, guid, number):
        DeleteNumberFromPhoneList(self.Whitelist, guid, number)
