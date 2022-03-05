##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## History
##

### INFRA
# Blacklist db import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus

### MODELS
# History Model import
from Models.Infrastructure.Factory.UserFactory.Lists.HistoryList import HistoryList
# Sub Model for HistoryCall Request import
from Models.Endpoints.Account.Lists.History.HistoryCallRequest import HistoryCallRequest


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


    def AddHistoryCall(self, HistoryCall: HistoryCallRequest):
        self.__HistoryDB.addHistoryCallForUser(
            self.__guid,
            HistoryCall.number,
            CallStatus.EnumToStr(HistoryCall.status),
            HistoryCall.time
        )
        return HistoryList(self.__HistoryDB.GetHistory(self.__guid))


    def DeleteHistoryCall(self, number: str, time: int):
        self.__HistoryDB.delHistoryCallForUser(
            self.__guid,
            number,
            time
        )
        return HistoryList(self.__HistoryDB.GetHistory(self.__guid))
