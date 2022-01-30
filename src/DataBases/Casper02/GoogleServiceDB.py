##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GoogleServiceDB
##

# Client mongo db import
import pymongo

# Import db name
from config import dbnameCasper02

# Melchior uri import!
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import GetDocument

# Object to represent table Contributors
class GoogleServiceDB():
    def __init__(self, db_name=dbnameCasper02):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.GoogleServices = self.db['GoogleServices']

    def PullGMailCreds(self):
        result = GetDocument(self.GoogleServices, "service", "GMail")
        if (result is None):
            return None
        return (result["credentials"]["email"], result["credentials"]["email"])
