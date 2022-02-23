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

from Logic.Services.PWDConvert.PWDConvert import PWDConvert

import uuid

class UserFactory():
    def __init__(self):
        self.__UserDB = UserDB()
        self.__BlackListDB = BlacklistDB()
        self.__WhiteListDB = WhitelistDB()
        self.__HistoryDB = HistoryDB()
        self.__PWDConvert = PWDConvert()


    def CreateUser(self, UserInfos):
        guid = str(uuid.uuid4())
        UserInfos = self.__EditUserInfos(UserInfos, guid)
        self.__CreateUserInDB(guid, UserInfos)
        self.__CreateUserLists(guid)
        return User(guid)


    def LoginUser(self, email, pwd):
        user = self.__UserDB.getUser(email)
        if user == None:
            return True, "this email is not linked to an account"
        if not self.__PWDConvert.Compare(pwd, user["password"]):
            return True, "you can not connect with this combination of email and password"
        return False, user["guid"]


    def LoadUser(guid):
        return User(guid)


    def __EditUserInfos(self, UserInfos, guid):
        UserInfos["guid"] = guid
        UserInfos["password"] = self.__PWDConvert.Serialize(UserInfos["password"])
        return UserInfos


    def __CreateUserInDB(self, UserInfos):
        self.__UserDB.addUser(UserInfos)


    def __CreateUserLists(self, guid):
        self.__BlackListDB.newBlacklist(guid)
        self.__WhiteListDB.newWhitelist(guid)
        self.__HistoryDB.newHistory(guid)
