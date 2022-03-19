##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryDB
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker
# Melchior Internal Utils
from Infrastructure.Services.MongoDB.Melchior.UserLists.UserListsWorker import UserListsWorker

### LOGIC
# Get env vars import
import os

# Object to represent table History
class HistoryDB():
    def __init__(self, db_name=os.getenv("DB_MELCHIOR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.History = self.db["History"]
        self.DBWatcher = MongoDBWatcher(self.History)
        self.DBWorker = MongoDBWorker(self.History)


    ### PUBLIC

    def newHistory(self, guid):
        NewHistoryDocument = {
            "guid": guid,
            "History": []
        }
        self.DBWorker.InsertDocument(NewHistoryDocument)


    def deleteHistory(self, guid):
        self.DBWorker.DeleteDocument(guid)


    def exists(self, guid):
        return self.DBWatcher.IsDocument("guid", guid)


    def getHistoryForUser(self, guid):
        return self.DBWatcher.GetDocument("guid", guid)


    def GetHistory(self, guid):
        return self.DBWatcher.GetDocument("guid", guid)["History"]


    def delHistoryCallForUser(self, guid: str, number: str, time: int):
        CurrentList = self.__PullList(guid)
        if CurrentList is None:
            return
        NewList = self.__DeleteHistoryCall(
            number,
            time,
            CurrentList["History"]
        )
        self.__UpdateList(guid, NewList)


    def addHistoryCallForUser(self, guid: str, number: str, status: str, time: int):
        CurrentList = self.__PullList(guid)
        if CurrentList is None:
            return
        NewList = self.__AddHistoryCall(
            number,
            status,
            time,
            CurrentList["History"]
        )
        self.__UpdateList(guid, NewList)


    ### PRIVATE

    def __PullList(self, guid: str):
        return self.DBWatcher.GetDocument("guid", guid)


    def __UpdateList(self, guid: str, NewList: list):
        QueryGUID = {
            'guid': str(guid)
        }
        QueryData = { "$set": { "History": NewList } }
        self.History.update_one(QueryGUID, QueryData)


    def __AddHistoryCall(self, number: str, status: str, time: int, TemporaryList: list):
        TemporaryList.append({
                "number": number,
                "status": status,
                "time": time
            }
        )
        return TemporaryList


    def __DeleteHistoryCall(self, number: str, time: int, TemporaryList: list):
        for i in range(len(TemporaryList)):
            if (TemporaryList[i]["number"] == number
            and TemporaryList[i]["time"] == time):
                del TemporaryList[i]
                return TemporaryList
        return TemporaryList
