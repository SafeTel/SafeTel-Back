##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Whitelist
##

### INFRA
# Blacklist db import
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
# Conflict Resolver for number in Lists
from Infrastructure.Factory.UserFactory.Lists.NumberConflictResolver import NumberConflictResolver

### MODELS
# PhoneList Model import
from Models.Infrastructure.Factory.UserFactory.Lists.PhoneList import PhoneList

# Represents Blacklist at high level usage
class Whitelist():
    def __init__(self, guid: str, WhitelistDB: WhitelistDB, ConflictResolver: NumberConflictResolver):
        self.__guid = guid
        self.__WhitelistDB = WhitelistDB
        self.__ConflictResolver = ConflictResolver

    def CreateWhitelist(self):
        self.__WhitelistDB.newWhitelist(self.__guid)

    def PullList(self):
        return PhoneList(self.__WhitelistDB.getWhitelistForUser(self.__guid))


    def AddNumber(self, number: str):
        if (self.__ConflictResolver.IsConflict(number)):
            self.__ConflictResolver.ResolveIntoWhitelist(number)
        else:
            self.__WhitelistDB.addWhitelistNumberForUser(number)
        return PhoneList(self.__WhitelistDB.getWhitelistForUser(self.__guid))


    def DeleteNumber(self, number: str):
        self.__WhitelistDB.delWhitelistNumberForUser(self.__guid, number)
        return PhoneList(self.__WhitelistDB.getWhitelistForUser(self.__guid))
