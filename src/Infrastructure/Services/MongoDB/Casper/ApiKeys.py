##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## ApiKeys
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWorker import MongoDBWorker

### LOGIC
# time import
import time
# env var import
import os

# Object to represent table Contributors
class ApiKeyLogDB():
    def __init__(self, db_name=os.getenv("DB_CASPER")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.ApiKeyLog = self.db['ApiKeyLog']
        self.DBWatcher = MongoDBWatcher(self.ApiKeyLog)
        self.DBWorker = MongoDBWorker(self.ApiKeyLog)

    def logClaimeApiKey(self, apiKey, name, ip):
        document = {
            "apiKey": apiKey,
            "name": name,
            "ip": ip,
            "ts": time.time()
        }
        return self.DBWorker.InsertDocument(document)

    def isApiKeyForContributor(self, name, ip):
        if (self.DBWatcher.IsDocument("name", name)
        or self.DBWatcher.IsDocument("ip", ip)):
            return True
        return False

    def isValidApiKey(self, apiKey):
        return self.DBWatcher.IsDocument("apiKey", apiKey)
