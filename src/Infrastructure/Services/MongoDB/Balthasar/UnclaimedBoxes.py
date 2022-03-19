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

# Object to represent table Contributors
class UnclaimedBoxesDB():
    def __init__(self, db_name=os.getenv("DB_BALTHASAR")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.UnclaimedBoxes = self.db['UnclaimedBoxes']
        self.DBWatcher = MongoDBWatcher(self.UnclaimedBoxes)
        self.DBWorker = MongoDBWorker(self.UnclaimedBoxes)


    def isValidBoxid(self, boxid: str):
        return self.DBWatcher.IsDocument("boxid", boxid)


    def deleteBoxid(self, boxid: str):
        self.DBWorker.DeleteDocumentByProp("boxid", boxid)
