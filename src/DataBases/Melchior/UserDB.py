##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## UserDB
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

# Object to represent table User
class UserDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Users = self.db['User']

    def addUser(self, user_data):
        InsertDocument(self.Users, user_data)

    def deleteUser(self, guid):
        DeleteDocument(self.Users, {'guid': guid})

    def exists(self, email):
        return IsDocument(self.Users, 'email', email)

    def getUser(self, email):
        return GetDocument(self.Users, 'email', email)

    def existByGUID(self, guid):
        return IsDocument(self.Users, 'guid', guid)

    def getUserByGUID(self, guid):
        return GetDocument(self.Users, 'guid', guid)
