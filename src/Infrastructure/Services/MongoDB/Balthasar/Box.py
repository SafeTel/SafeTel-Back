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

### LOGIC
# env var import
import os

# Object to represent table Contributors
class BoxesDB():
    def __init__(self, db_name=os.getenv("DB_BALTHASAR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Box = self.db['Box']
        self.DBWatcher = MongoDBWatcher(self.Box)
        self.DBWorker = MongoDBWorker(self.Box)


    def createDataBox(self, boxdata: dict):
        self.DBWorker.InsertDocument(boxdata)


    def addBox(self, boxdata: dict):
        return # update the box list


    def getBoxData(self, guid: str):
        self.DBWatcher.GetDocument("guid", guid)


    def isBox(self, guid: str):
        self.DBWatcher.IsDocument("guid", guid)


    def delete(self, guid: str):
        self.DBWorker.DeleteDocument(guid)
