##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Contributors
##

# Client mongo db import
import pymongo

# Import db name
from config import dbnameCasper

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import IsDocument

# Object to represent table Contributors
class ContributorsDB():
    def __init__(self, db_name=dbnameCasper):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Contributors = self.db['Contributors']

    def IsContributor(self, name):
        return IsDocument(self.Contributors, 'name', name)
