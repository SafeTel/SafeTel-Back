##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## History
##

### INFRA
# Blacklist db import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
# Conflict Resolver for number in Lists
from Infrastructure.Factory.UserFactory.Lists.NumberConflictResolver import NumberConflictResolver

### MODELS
# History Model import
from Models.Infrastructure.Factory.UserFactory.Lists.HistoryList import HistoryList

### /!\ WARNING /!\ ###
# This is an HIGH LEVEL Blacklist INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###

# Represents Blacklist at high level usage
class History():
    def __init__(self, guid: str, HistoryDB: HistoryDB):
        self.__guid = guid
        self.__HistoryDB = HistoryDB


    def CreateBlacklist(self):
        self.__HistoryDB.newHistory(self.__guid)


    def PullList(self):
        return HistoryList(self.__HistoryDB.GetHistory(self.__guid))


    def AddNumber(self, number: str):
        #self.__HistoryDB.addHistoryCallForUser()
        return HistoryList(self.__HistoryDB.GetHistory(self.__guid))


    def DeleteNumber(self, number: str):
        #self.__HistoryDB.delHistoryCallForUser(self.__guid, number)
        return HistoryList(self.__HistoryDB.GetHistory(self.__guid))
