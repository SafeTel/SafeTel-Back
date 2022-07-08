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

    ### PUBLIC

    ## READ
    def getNumber(self, number: str):
        return self.__PullNumber(number)


    def isNumber(self, number: str):
        return self.DBWatcher.IsDocument('number', number)


    def count(self):
        return self.NumberDB.count_documents({})


    ## WRITE

    def UpdateScore(self, number: str, newScore: int):
        self.__UpdateScore(number, newScore)


    def addCall(self, number: str):
        Current = self.__PullNumber(number)
        if Current is None:
            return
        self.__UpdateDocumentCalls(
            number,
            Current["calls"] + 1,
            Current["reportedcalls"],
            Current["blockedcalls"]
        )


    def addBlockedCall(self, number: str):
        Current = self.__PullNumber(number)
        if Current is None:
            return
        self.__UpdateDocumentCalls(
            number,
            Current["calls"] + 1,
            Current["reportedcalls"],
            Current["blockedcalls"] + 1
        )


    def reportNumber(self, number: str, guid: str, boxid: str):
        Current = self.__PullNumber(number)
        if Current is None:
            return
        NewList = self.__AddReport(
            guid,
            boxid,
            Current["Reports"]
        )
        self.__UpdateDocumentReports(
            number,
            NewList,
            Current["calls"] + 1,
            Current["reportedcalls"] + 1
        )


    ## CREATE

    def addNumber(self, number: str, TellowsResponse: dict, guid: str, boxid: str, score: int = 5):
        Document = {
            "number": number,
            "identifier": self.identifier,
            "score": int(score),
            "calls": 0,
            "reportedcalls": 0,
            "blockedcalls": 0,
            "Reports": [
                {
                    "guid": guid,
                    "boxid": boxid,
                    "timestamp": time.time()
                }
            ],
            "TellowsResponse": TellowsResponse
        }
        self.DBWorker.InsertDocument(Document)


    def addNumberWithoutReport(self, number: str, TellowsResponse: dict, score: int = 5):
        Document = {
            "number": number,
            "identifier": self.identifier,
            "score": int(score),
            "calls": 0,
            "reportedcalls": 0,
            "blockedcalls": 0,
            "Reports": [],
            "TellowsResponse": TellowsResponse
        }
        self.DBWorker.InsertDocument(Document)

    ### PRIVATE

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


    def __UpdateScore(self, number: str, newScore: int):
        QueryDocument = {
            'number': str(number)
        }
        QueryData = {
            "$set": {
                "score": newScore
            }
        }
        self.NumberDB.update_one(QueryDocument, QueryData)


    def __UpdateDocumentReports(self, number: str, NewList: list, calls: int, reportedcalls: int):
        QueryDocument = {
            'number': str(number)
        }
        QueryData = {
            "$set": {
                "Reports": NewList,
                "calls": calls,
                "reportedcalls": reportedcalls
            }
        }
        self.NumberDB.update_one(QueryDocument, QueryData)


    def __UpdateDocumentCalls(self, number: str, calls: int, reportedcall: int, blockedcall: int):
        QueryDocument = {
            'number': str(number)
        }
        QueryData = {
            "$set": {
                "calls": calls,
                "reportedcalls": reportedcall,
                "blockedcalls": blockedcall,
            }
        }
        self.NumberDB.update_one(QueryDocument, QueryData)
