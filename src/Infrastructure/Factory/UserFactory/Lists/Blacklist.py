##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Blacklist
##

### INFRA
# Blacklist db import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
# Conflict Resolver for number in Lists
from Infrastructure.Factory.UserFactory.Lists.NumberConflictResolver import NumberConflictResolver

### MODELS
# PhoneList Model import
from Models.Infrastructure.Factory.UserFactory.Lists.PhoneList import PhoneList


### /!\ WARNING /!\ ###
# This is an HIGH LEVEL Blacklist INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Represents Blacklist at high level usage
class Blacklist():
    def __init__(self, guid: str, BlacklistDB: BlacklistDB, ConflictResolver: NumberConflictResolver):
        self.__guid = guid
        self.__BlacklistDB = BlacklistDB
        self.__ConflictResolver = ConflictResolver


    def CreateBlacklist(self):
        self.__BlacklistDB.newBlacklist(self.__guid)


    def PullList(self):
        return PhoneList(self.__BlacklistDB.GetBlacklistNumbers(self.__guid))


    def AddNumber(self, number: str):
        BlacklistNumbers = PhoneList(self.__BlacklistDB.GetBlacklistNumbers(self.__guid))

        if (self.__IsNumberInList(number, BlacklistNumbers)):
            return BlacklistNumbers

        if (self.__ConflictResolver.IsConflictForBlacklist(number)):
            self.__ConflictResolver.ResolveIntoBlacklist(number)
        else:
            self.__BlacklistDB.addBlacklistNumberForUser(self.__guid, number)

        return PhoneList(self.__BlacklistDB.GetBlacklistNumbers(self.__guid))


    def DeleteNumber(self, number: str):
        self.__BlacklistDB.delBlacklistNumberForUser(self.__guid, number)
        return PhoneList(self.__BlacklistDB.GetBlacklistNumbers(self.__guid))


    def __IsNumberInList(self, targetnumber: str, PhoneList: PhoneList):
        return targetnumber in PhoneList.PhoneNumbers
