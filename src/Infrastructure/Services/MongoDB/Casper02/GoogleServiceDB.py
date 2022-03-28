##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GoogleServiceDB
##

### INFRA
# Client mongo db import
import pymongo
# MongoDBMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher

### LOGIC
# env vars import
import os

# Object to represent table Contributors
class GoogleServiceDB():
    def __init__(self, db_name=os.getenv("DB_CASPER_02")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.GoogleServices = self.db['GoogleServices']
        self.DBWatcher = MongoDBWatcher(self.GoogleServices)


    def PullGMailCreds(self):
        result = self.DBWatcher.GetDocument("service", "GMail")
        if (result is None):
            return None
        return (result["credentials"]["email"], result["credentials"]["password"])
