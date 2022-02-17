##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Contributors
##

# Client mongo db import
import pymongo

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import IsDocument

import os

# Object to represent table Contributors
class ContributorsDB():
    def __init__(self, db_name=os.getenv("DB_CASPER")):
        self.client = pymongo.MongoClient(os.getenv("DB_URI"))
        self.db = self.client[db_name]
        self.Contributors = self.db['Contributors']

    def IsContributor(self, name):
        return IsDocument(self.Contributors, 'name', name)
