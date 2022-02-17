##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GoogleServiceDB
##

# Client mongo db import
import pymongo

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument

import os

# Object to represent table Contributors
class GoogleServiceDB():
    def __init__(self, db_name=os.getenv("DB_CASPER_02")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.GoogleServices = self.db['GoogleServices']

    def PullGMailCreds(self):
        result = GetDocument(self.GoogleServices, "service", "GMail")
        if (result is None):
            return None
        return (result["credentials"]["email"], result["credentials"]["password"])
