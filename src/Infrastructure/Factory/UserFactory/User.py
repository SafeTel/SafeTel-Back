##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## User
##

### INFRA
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

class User():
    def __init__(self, guid):
        self.__UserDB = UserDB()
        self.__BlackListDB = BlacklistDB()
        self.__WhiteListDB = WhitelistDB()
        self.__HistoryDB = HistoryDB()
        self.__guid = guid
        self.__UserInfos = None


    # READ
    def GetGUID(self):
        return self.__guid


    def PullUserInfos(self):
        return self.__MandaroryUserInfosPull()


    def __MandaroryUserInfosPull(self):
        if (self.__UserInfos == None):
            self.__UserInfos = self.__UserDB.getUserByGUID(self.__guid)
        return self.__UserInfos


    # UPDATE
    def UpdateEmail(self, newEmail):
        self.__MandaroryUserInfosPull()
        self.__UserDB.UpdateAccountEmail(self.__guid, newEmail)


    def UpdatePersonalInfos(self, NewUserInfos):
        self.__MandaroryUserInfosPull()
        NewCustomerInfos = NewUserInfos["customerInfos"]
        NewLocalization = NewUserInfos["localization"]
        self.__UserDB.UpdatePersonalInfos(self.__guid, NewCustomerInfos, NewLocalization)


    # DELETE
    def Delete(self):
        self.__UserDB.deleteUser(self.__guid)
        self.__BlackListDB.deleteBlacklist(self.__guid)
        self.__WhiteListDB.deleteWhitelist(self.__guid)
        self.__HistoryDB.deleteHistory(self.__guid)


    def IsDeleted(self):
        if (self.__BlackListDB.exists(self.__guid)
        or self.__WhiteListDB.exists(self.__guid)
        or self.__HistoryDB.exists(self.__guid)
        or self.__UserDB.existByGUID(self.__guid)):
            return False
        return True
