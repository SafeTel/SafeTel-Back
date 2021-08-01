##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## BlackListDB
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

# Melchior Internal Utils
from DataBases.Melchior.InternalUtils.DataWorker import AddNumberToPhoneList, DeleteNumberFromPhoneList

# Object to represent table Blacklist
class BlacklistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
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
