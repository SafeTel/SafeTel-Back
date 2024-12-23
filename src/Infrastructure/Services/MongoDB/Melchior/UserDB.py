##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UserDB
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker
from Infrastructure.Services.MongoDB.Melchior.UserDBWatcher import UserDBWatcher
from Infrastructure.Services.MongoDB.Melchior.UserDBWorker import UserDBWorker
# Roles import
from Models.Logic.Shared.Roles import Roles

### LOGIC
# Get env vars
import os


class UserDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Users = self.db['User']
        self.DBWatcher = MongoDBWatcher(self.Users)
        self.DBWorker = MongoDBWorker(self.Users)
        self.DBUserWatcher = UserDBWatcher(self.Users)
        self.DBUserWorker = UserDBWorker(self.Users)


    def addUser(self, user_data: dict, role: Roles):
        if ("magicnumber" in user_data):
            del user_data["magicnumber"]
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
        return self.DBUserWatcher.GetAccountsByRole(target)


    def deleteUser(self, guid: str):
        self.DBWorker.DeleteDocument(guid)


    def exists(self, email: str):
        return self.DBWatcher.IsDocument('email', email)


    def getUser(self, email: str):
        return self.DBWatcher.GetDocument('email', email)


    def existByGUID(self, guid: str):
        return self.DBWatcher.IsDocument('guid', guid)


    def getUserByGUID(self, guid: str):
        return self.DBWatcher.GetDocument('guid', guid)


    def getUserRoleByGUID(self, guid: str):
        return self.DBWatcher.GetDocument('guid', guid)['role']


    def UpdateLostPasswordMode(self, guid: str, mode: bool):
        self.DBUserWorker.ChangeToLostPasswordMode(guid, mode)


    def UpdateLostPassword(self, guid: str, newpassword: str):
        self.DBUserWorker.UpdateLostPassword(guid, newpassword)


    def UpdateAccountEmail(self, guid: str, email: str):
        self.DBUserWorker.UpdateAccountEmail(guid, email)


    def UpdatePersonalInfos(self, guid: str, customerInfos: dict, localization: dict):
        self.DBUserWorker.UpdatePersonalInfos(guid, customerInfos, localization)
