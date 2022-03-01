##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## UserFactory
##


from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

from Infrastructure.Factory.UserFactory.User import User
from Models.Logic.Shared.Roles import Roles

from Logic.Services.PWDConvert.PWDConvert import PWDConvert

from Models.Endpoints.Authentification.RegisterRequest import RegisterRequest

import uuid

class UserFactory():
    def __init__(self):
        self.__UserDB = UserDB()
        self.__BlackListDB = BlacklistDB()
        self.__WhiteListDB = WhitelistDB()
        self.__HistoryDB = HistoryDB()
        self.__PWDConvert = PWDConvert()


    def CreateUser(self, UserInfos: RegisterRequest):
        if (self.__IsUser(guid)):
            return None
        guid = str(uuid.uuid4())
        UserInfosEdited = self.__EditUserInfos(UserInfos, guid)
        self.__CreateUserInDB(UserInfosEdited)
        self.__CreateUserLists(guid)
        return User(guid)


    def LoginUser(self, email: str, pwd: str):
        user = self.__UserDB.getUser(email)
        if (user == None):
            return True, "This email is not linked to an account"
        if (not self.__PWDConvert.Compare(pwd, user["password"])):
            return True, "You can not connect with this combination of email and password"
        return False, user["guid"]


    def LoadUser(self, guid: str):
        if (not self.__IsUser(guid)):
            return None
        return User(guid)


    def __IsUser(self, guid: str):
        return self.__UserDB.existByGUID(guid)


    def __EditUserInfos(self, UserInfos: RegisterRequest, guid: str):
        UserInfosDict = UserInfos.ToDict()
        UserInfosDict["guid"] = guid
        UserInfosDict["password"] = self.__PWDConvert.Serialize(UserInfos.password)
        return UserInfosDict


    def __CreateUserInDB(self, UserInfos: dict):
        self.__UserDB.addUser(UserInfos, Roles.USER)


    def __CreateUserLists(self, guid: str):
        self.__BlackListDB.newBlacklist(guid)
        self.__WhiteListDB.newWhitelist(guid)
        self.__HistoryDB.newHistory(guid)
