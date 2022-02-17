##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## UserDB
##

# Client mongo db import
import pymongo

# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker
from DataBases.Melchior.InternalUtils.DataWorker import GetAccountsByRole

# Roles import
from Logic.Models.Roles import Roles

import os

# Object to represent table User
class UserDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Users = self.db['User']
        self.DBWatcher = MongoDBWatcher(self.Users)
        self.DBWorker = MongoDBWorker(self.Users)

    def addUser(self, user_data, role):
        del user_data["magicNumber"]
        if (role == Roles.USER):
            user_data['role'] = 'user'
        elif (role == Roles.DEVELOPER):
            user_data['role'] = 'developer'
        elif (role == Roles.ADMIN):
            user_data['role'] = 'admin'
        self.DBWorker.InsertDocument(user_data)

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
        self.DBWorker.DeleteDocument({'guid': guid})

    def exists(self, email):
        return self.DBWatcher.IsDocument('email', email)

    def getUser(self, email):
        return self.DBWatcher.GetDocument('email', email)

    def existByGUID(self, guid):
        return self.DBWatcher.IsDocument('guid', guid)

    def getUserByGUID(self, guid):
        return self.DBWatcher.GetDocument('guid', guid)

    def getUserRoleByGUID(self, guid):
        return self.DBWatcher.GetDocument('guid', guid)['role']
