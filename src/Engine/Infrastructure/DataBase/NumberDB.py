##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## CountryDB
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

### LOGIC
# env var import
import os
# timestamp generation
import time

# Object to represent table NumberDB
class NumberDB():
    def __init__(self, country_id: str, identifier: str, db_name=os.getenv("DB_BALTHASAR_02")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.NumberDB = self.db[country_id]
        self.DBWatcher = MongoDBWatcher(self.NumberDB)
        self.DBWorker = MongoDBWorker(self.NumberDB)
        self.identifier = identifier


    def getNumber(self, number: str):
        return self.__PullNumber(number)


    def isNumber(self, number: str):
        return self.DBWatcher.IsDocument('number', number)


    def reportNumber(self, number: str, guid: str, boxid: str):
        Current = self.__PullNumber(number)
        if Current is None:
            return
        NewList = self.__AddReport(
            guid,
            boxid,
            Current["Reports"]
        )
        self.__UpdateList(number, NewList)


    def addNumber(self, number: str, guid: str, boxid: str, score: int):
        Document = {
            "number": number,
            "identifier": self.identifier,
            "score": score,
            "source": "User",
            "Reports": [
                {
                    "guid": guid,
                    "boxid": boxid,
                    "timestamp": time.time()
                }
            ]
        }
        self.DBWorker.InsertDocument(Document)


    # addNumberFromTellows: TODO: See if there is any interest to make the difference

    # PRIVATE

    def __PullNumber(self, number: str):
        return self.DBWatcher.GetDocument('number', number)


    def __AddReport(self, guid: str, boxid: str, TemporaryList: list):
        TemporaryList.append({
                "guid": guid,
                "boxid": boxid,
                "timestamp": time.time()
            }
        )
        return TemporaryList


    def __UpdateList(self, number: str, NewList: list):
        QueryNumber = {
            'number': str(number)
        }
        QueryData = {
            "$set": { "Reports": NewList }
        }
        self.NumberDB.update_one(QueryNumber, QueryData)
