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

# Object to represent conflict in Lists and resolve them
class NumberConflictResolver():
    def __init__(self, guid: str, BlacklistDB: BlacklistDB, WhitelistDB: WhitelistDB):
        self.__guid = guid
        self.__BlacklistDB = BlacklistDB
        self.__WhitekistDB = WhitelistDB
        self.__BlacklistNumbers = None
        self.__WhitelistNumbers = None


    def ExistInList(self, number: str):
        self.__PullLists()
        if (self.__IsNumberInList(number, self.__BlacklistNumbers)
        or self.__IsNumberInList(number, self.__WhitelistNumbers)):
            return True
        return False


    def IsConflictForBlacklist(self, number: str):
        self.__PullLists()
        return self.__IsNumberInList(number, self.__WhitelistNumbers)


    def IsConflictForWhitelist(self, number: str):
        self.__PullLists()
        return self.__IsNumberInList(number, self.__BlacklistNumbers)


    def ResolveIntoBlacklist(self, number: str):
        self.__WhitekistDB.delWhitelistNumberForUser(self.__guid, number)
        self.__BlacklistDB.addBlacklistNumberForUser(self.__guid, number)


    def ResolveIntoWhitelist(self, number: str):
        self.__BlacklistDB.delBlacklistNumberForUser(self.__guid, number)
        self.__WhitekistDB.addWhitelistNumberForUser(self.__guid, number)


    def __PullLists(self):
        self.__BlacklistNumbers = PhoneList(self.__BlacklistDB.GetBlacklistNumbers(self.__guid))
        self.__WhitelistNumbers = PhoneList(self.__WhitekistDB.GetBWhitelistNumbers(self.__guid))


    def __IsNumberInList(self, targetnumber: str, PhoneList: PhoneList):
        return targetnumber in PhoneList.PhoneNumbers
