##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## ApiKeys
##

# Client mongo db import
import pymongo

# Import db name
from config import dbnameCasper

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# PyMongo Internal Utils
from DataBases.InternalUtils.DataWatcher import IsDocument
from DataBases.InternalUtils.DataWorker import InsertDocument

# time import
import time

# Object to represent table Contributors
class ApiKeyLogDB():
    def __init__(self, db_name=dbnameCasper):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.ApiKeyLog = self.db['ApiKeyLog']

    def logClaimeApiKey(self, apiKey, name, ip):
        document = {
            "apiKey": apiKey,
            "name": name,
            "ip": ip,
            "ts": time.time()
        }
        return InsertDocument(self.ApiKeyLog, document)

    def isApiKeyForContributor(self, name, ip):
        if (IsDocument(self.ApiKeyLog, "name", name)
        or IsDocument(self.ApiKeyLog, "ip", ip)):
            return True
        return False
