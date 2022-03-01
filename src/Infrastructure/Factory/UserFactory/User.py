##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## User
##

### INFRA
# User db import
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
# Lists db imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
### MODELS
# UserInfos JParent imort
from Models.Infrastructure.Factory.UserFactory.UserInfos import UserInfos
# Shared JObject import
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

class User():
    def __init__(self, guid: str):
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
        return self.__PullUserInfos()


    def Exists(self):
        return self.__UserDB.existByGUID()


    def __PullUserInfos(self):
        if (self.__UserInfos == None):
            userRaw = self.__UserDB.getUserByGUID(self.__guid)
            self.__UserInfos = UserInfos(userRaw)
        return self.__UserInfos


    # UPDATE
    def UpdateEmail(self, newEmail: str):
        self.__PullUserInfos()
        self.__UserDB.UpdateAccountEmail(self.__guid, newEmail)


    def UpdatePersonalInfos(self, CustomerInfos: CustomerInfos, Localization: Localization):
        self.__PullUserInfos()
        NewCustomerInfos = CustomerInfos.ToDict()
        NewLocalization = Localization.ToDict()
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
