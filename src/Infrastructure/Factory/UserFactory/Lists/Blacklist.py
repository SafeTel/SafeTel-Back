##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Blacklist
##

# Lists db imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB

class Blacklist():
    def __init__(self, guid: str, BlacklistDB: BlacklistDB):
        self.__guid = guid
        self.__BlacklistDB = BlacklistDB

    def PullList(self):
        return self.__BlacklistDB.getBlacklistForUser(self.__guid)

    def AddNumber(self, number: str):
        self.__BlacklistDB.addBlacklistNumberForUser(number)
        return self.__BlacklistDB.getBlacklistForUser(self.__guid)
