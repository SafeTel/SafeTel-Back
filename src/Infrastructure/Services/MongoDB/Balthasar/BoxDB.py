##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Boxes
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

### MODELS
# Box Model import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity

### LOGIC
# env var import
import os

# Object to represent table Box
class BoxDB():
    def __init__(self, db_name=os.getenv("DB_BALTHASAR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Box = self.db['Boxes']
        self.DBWatcher = MongoDBWatcher(self.Box)
        self.DBWorker = MongoDBWorker(self.Box)


    ### PÜBLIC

    def newDataBox(self, guid: str):
        NewBoxDocument = {
            "guid": guid,
            "Boxes": []
        }
        self.DBWorker.InsertDocument(NewBoxDocument)


    def getBoxData(self, guid: str):
        return self.DBWatcher.GetDocument("guid", guid)


    def isBox(self, guid: str):
        return self.DBWatcher.IsDocument("guid", guid)


    def delete(self, guid: str):
        self.DBWorker.DeleteDocument(guid)


    def addBox(self, guid: str, boxid: str, call: bool, activity: bool, severity: str):
        Current = self.__PullData(guid)
        if Current is None:
            return
        NewList = self.__AddBox(
            boxid,
            call,
            activity,
            severity,
            Current["Boxes"]
        )
        self.__UpdateList(guid, NewList)


    def updateBoxes(self, guid: str, UserBoxes: list):
        for UserBox in UserBoxes:
            UserBox["severity"] = BoxSeverity.EnumToStr(UserBox["severity"])
        self.__UpdateList(guid, UserBoxes)


    def RSUserByBoxID(self, boxid: str):
        result =  self.Box.find({'Boxes': {'$elemMatch': {'boxid':boxid}}})
        for tmp in result:
            return tmp["guid"]
        return None


    def RSByBoxID(self, boxid: str):
        result =  self.Box.find({'Boxes': {'$elemMatch': {'boxid':boxid}}})
        for tmp in result:
            return tmp
        return None


    ### PRIVATE

    def __PullData(self, guid: str):
        return self.DBWatcher.GetDocument("guid", guid)


    def __AddBox(self, boxid: str, call: bool, activity: bool, severity: str, TemporaryList: list):
        TemporaryList.append({
                "boxid": boxid,
                "call": call,
                "ip": "",
                "activity": activity,
                "severity": severity,
                "Reports":[]
            }
        )
        return TemporaryList


    def __UpdateList(self, guid: str, NewList: list):
        QueryGUID = {
            'guid': str(guid)
        }
        QueryData = {
            "$set": { "Boxes": NewList }
        }
        self.Box.update_one(QueryGUID, QueryData)
