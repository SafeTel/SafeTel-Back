##
## EPITECH PROJECT, 2022
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

# Represents Blacklist at high level usage
class Blacklist():
    def __init__(self, guid: str, BlacklistDB: BlacklistDB, ConflictResolver: NumberConflictResolver):
        self.__guid = guid
        self.__BlacklistDB = BlacklistDB
        self.__ConflictResolver = ConflictResolver


    def PullList(self):
        return PhoneList(self.__BlacklistDB.getBlacklistForUser(self.__guid))


    def AddNumber(self, number: str):
        if (self.__ConflictResolver.IsConflict(number)):
            self.__ConflictResolver.ResolveIntoBlacklist(number)
        else:
            self.__BlacklistDB.addBlacklistNumberForUser(number)
        return PhoneList(self.__BlacklistDB.getBlacklistForUser(self.__guid))


    def DeleteNumber(self, number: str):
        self.__BlacklistDB.delBlacklistNumberForUser(self.__guid, number)
        return PhoneList(self.__BlacklistDB.getBlacklistForUser(self.__guid))
