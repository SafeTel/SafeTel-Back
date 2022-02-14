##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## UserDB
##

# Client mongo db import
import pymongo

# Import db name and db URI
from config import dbname, URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument, IsDocument
from DataBases.InternalUtils.DataWorker import InsertDocument, DeleteDocument
from DataBases.Melchior.InternalUtils.DataWorker import GetAccountsByRole

# Roles import
from Logic.Models.Roles import Roles

# Object to represent table User
class UserDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Users = self.db['User']

    def addUser(self, user_data, role):
        del user_data["magicNumber"]
        if (role == Roles.USER):
            user_data['role'] = 'user'
        elif (role == Roles.DEVELOPER):
            user_data['role'] = 'developer'
        elif (role == Roles.ADMIN):
            user_data['role'] = 'admin'
        InsertDocument(self.Users, user_data)

    def getUsersByRole(self, role):
        target = ""
        if (role == Roles.USER):
            target = "user"
        elif(role == Roles.DEVELOPER):
            target = "developer"
        elif(role == Roles.ADMIN):
            target = "admin"
        return GetAccountsByRole(self.Users, target)

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

    def getUserRoleByGUID(self, guid):
        return GetDocument(self.Users, 'guid', guid)['role']
