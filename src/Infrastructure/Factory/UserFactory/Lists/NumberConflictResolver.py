##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ConflictNumberTroubleShooter
##

# Lists db imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

class NumberConflictResolver():
    def __init__(self, BlacklistDB: BlacklistDB, WhitelistDB: WhitelistDB):
        self.__BlackListDB = BlacklistDB
        self.__WhiteListDB = WhitelistDB

    def IsConflict(self, number: str):
        Blacklist = self.__BlackListDB.getBlacklistForUser(self.__guid)
        Whitelist = self.__WhiteListDB.getWhitelistForUser(self.__guid)
        



