##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Contributors
##

### INFRA
# Client mongo db import
import pymongo
# PyMongo Internal Utils
from Infrastructure.Services.MongoDB.InternalUtils.MongoDBWatcher import MongoDBWatcher

### LOGIC
# env vars import
import os

class ContributorsDB():
    def __init__(self, db_name=os.getenv("DB_CASPER")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Contributors = self.db['Contributors']
        self.DBWatcher = MongoDBWatcher(self.Contributors)


    def IsContributor(self, name):
        return self.DBWatcher.IsDocument('name', name)
