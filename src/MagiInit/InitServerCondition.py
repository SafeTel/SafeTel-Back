##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitServerCondition
##

### LOGIC
import logging
# env var import
import os
import json
# Regex
import re
from tkinter.messagebox import NO

### INFRA
# Client mongo db import
import pymongo
# Error for exception
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class InitServerCondition():
    def __init__(self):
        self.__CheckMongoURI()
        self.__CheckMongoClientConnection()

    # Connect a client and perform a command to see if it's working
    def __CheckMongoURI(self):
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            launchMode = config["Mode"]["launchMode"]
            dbURI = os.getenv("DB_URI")
            if launchMode == "POSTMAN":
                postmanRegexMatchingResult = re.search("postman", dbURI)
                if postmanRegexMatchingResult == None:
                    raise Exception("Postman Launching mode: DB URI does not reach postman cluster")
            elif launchMode == "DEV":
                devRegexMatchingResult = re.search("dev", dbURI)
                if devRegexMatchingResult == None:
                    raise Exception("Dev Launching mode: DB URI does not reach dev cluster")

            elif launchMode == "PROD":
                postmanRegexMatchingResult = re.search("postman", dbURI)
                devRegexMatchingResult = re.search("dev", dbURI)
                if (postmanRegexMatchingResult != None 
                    or  devRegexMatchingResult != None):
                    raise Exception("Prod Launching mode: DB URI does not reach prod cluster")

    # Connect a client and perform a command to see if it's working
    def __CheckMongoClientConnection(self):
        try:
            client = pymongo.MongoClient(os.getenv("DB_URI"))
            # The ping command is cheap and does not require auth.
            logging.warning(client.admin.command('ping'))

        except ServerSelectionTimeoutError:
            raise Exception("Server not connected: Required Valid IP")

        except ConnectionFailure:
            raise Exception("Server not available")
