##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UnclaimedBoxes
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

# Object to represent table Unclaimed Boxes
class UnclaimedBoxsDB():
    def __init__(self, db_name=os.getenv("DB_BALTHASAR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.UnclaimedBoxs = self.db['UnclaimedBoxes']
        self.DBWatcher = MongoDBWatcher(self.UnclaimedBoxs)
        self.DBWorker = MongoDBWorker(self.UnclaimedBoxs)


    def isValidBoxid(self, boxid: str):
        return self.DBWatcher.IsDocument("boxid", boxid)


    def deleteByBoxid(self, boxid: str):
        self.DBWorker.DeleteDocumentByProp("boxid", boxid)
