##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ConflictNumberTroubleShooter
##

### INFRA
# Lists db imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

### MODELS
# PhoneList Model import
from Models.Infrastructure.Factory.UserFactory.Lists.PhoneList import PhoneList

class NumberConflictResolver():
    def __init__(self, guid: str, BlacklistDB: BlacklistDB, WhitelistDB: WhitelistDB):
        self.__guid = guid
        self.__BlacklistDB = BlacklistDB
        self.__WhitekistDB = WhitelistDB
        self.__Blacklist = None
        self.__Whitelist = None


    def ExistInList(self, number: str):
        self.__PullLists()
        if (self.__FindNumberInList(number, self.__Blacklist)
        or self.__FindNumberInList(number, self.__Whitelist)):
            return True
        return False


    def IsConflict(self, number: str):
        self.__PullLists()
        if (self.__FindNumberInList(number, self.__Blacklist)
        and self.__FindNumberInList(number, self.__Whitelist)):
            return True
        return False


    def ResolveIntoBlacklist(self, number: str):
        self.__WhitekistDB.delWhitelistNumberForUser(self.__guid, number)
        self.__BlacklistDB.addBlacklistNumberForUser(self.__guid, number)


    def ResolveIntoWhitelist(self, number: str):
        self.__BlacklistDB.delBlacklistNumberForUser(self.__guid, number)
        self.__WhitekistDB.addWhitelistNumberForUser(self.__guid, number)


    def __PullLists(self):
        self.__Blacklist = PhoneList(self.__BlacklistDB.getBlacklistForUser(self.__guid)["PhoneNumbers"])
        self.__Whitelist = PhoneList(self.__WhitekistDB.getWhitelistForUser(self.__guid)["PhoneNumbers"])


    def __FindNumberInList(self, number: str, PhoneList: PhoneList):
        return any(number in string for string in PhoneList.PhoneNumbers)
