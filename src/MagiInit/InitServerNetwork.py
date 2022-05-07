##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitServerCondition
##

### LOGIC
# env var import
import os
import json

### INFRA
# Client mongo db import
import pymongo


# Verify the Network integrity to launch Magi
class InitServerNetwork():
    def __init__(self):
        self.__UriBasePostman = "safetel-back-postman-cl"
        self.__UriBaseDev = "safetel-back-dev-cluste"
        self.__UriBaseProd = "safetel-back-cluster"

        launchMode = self.__VerifyDBUri()

        self.__VerifyDBAccess()


    # Verify the DB Uri
    def __VerifyDBUri(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        launchMode = self.__GetLaunchMode()
        if (launchMode != self.__EvaluateDBUri()):
            raise ValueError("FATAL ERROR: INVALID LAUNCH MODE")


    def __GetLaunchMode(self):
        launchMode = ""
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            launchMode = config["Mode"]["launchMode"]
        return launchMode


    def __EvaluateDBUri(self):
        DBUri = os.getenv("DB_URI")
        if (self.__UriBasePostman in DBUri):
            return "POSTMAN"
        if (self.__UriBaseDev in DBUri):
            return "DEV"
        if (self.__UriBaseProd in DBUri):
            return "PROD"
        raise ValueError("FATAL ERROR: INVALID LAUNCH MODE")



    # Verify that the current machine is allowed to run Magi
    def __VerifyDBAccess(self):
        try:
            client = pymongo.MongoClient(os.getenv("DB_URI"))
            client.admin.command('ping')
        except:
            raise ValueError("FATAL ERROR: YOU ARE NOT ALLOWED TO LAUNCH THE SERVER BY YOURSELF")
