##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## User
##

### INFRA
# User db internal usage import
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
# Lists db internal usage imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
# High level DB usage import
from Infrastructure.Factory.UserFactory.Lists.Blacklist import Blacklist
from Infrastructure.Factory.UserFactory.Lists.Whitelist import Whitelist
from Infrastructure.Factory.UserFactory.Lists.History import History
from Infrastructure.Factory.UserFactory.Box import FactBox
# Number Lists Conflict Resolver High level usage import
from Infrastructure.Factory.UserFactory.Lists.NumberConflictResolver import NumberConflictResolver

### MODELS
# UserInfos JParent imort
from Models.Infrastructure.Factory.UserFactory.UserInfos import UserInfos
# Shared JObject import
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

### LOGIC
# Password converter import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert


### /!\ WARNING /!\ ###
# This is an HIGH LEVEL User INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Class to represents the usage of a user inside the server (Worker)
class User():
    def __init__(self, guid: str):
        self.__guid = guid
        self.__UserInfos = None

        self.__PWDConvert = PWDConvert()

        self.__UserDB = UserDB()
        self.__HistoryDB = HistoryDB()
        self.__BlackListDB = BlacklistDB()
        self.__WhiteListDB = WhitelistDB()

        ConflictResolver = NumberConflictResolver(self.__guid, self.__BlackListDB, self.__WhiteListDB)

        self.Blacklist = Blacklist(self.__guid, self.__BlackListDB, ConflictResolver)
        self.Whitelist = Whitelist(self.__guid, self.__WhiteListDB, ConflictResolver)
        self.History = History(self.__guid, self.__HistoryDB)

        self.Box = FactBox(self.__guid)


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

    # SECURITY
    def LostPasswordMode(self, mode: bool = False):
        self.__UserDB.UpdateLostPasswordMode(self.__guid, mode)


    def UpdatePassword(self, newpassword: str):
        hashedpassword = self.__PWDConvert.Serialize(newpassword)
        self.__UserDB.UpdateLostPassword(self.__guid, hashedpassword)


    # UPDATE
    def UpdateEmail(self, newEmail: str):
        self.__UserDB.UpdateAccountEmail(self.__guid, newEmail)


    def UpdatePersonalInfos(self, CustomerInfos: CustomerInfos, Localization: Localization):
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
