##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitServerNetwork
##

### LOGIC
# Read env var import
import os
# Read config.json
import json
# Read branch name
from pygit2 import Repository

### INFRA
# Client mongo db import
import pymongo


# Verify the Network integrity to launch Magi
class InitServerNetwork():
    def __init__(self):
        self.__UriBasePostman = "safetel-back-postman-cl"
        self.__UriBaseDev = "safetel-back-dev-cluste"
        self.__UriBaseProd = "safetel-back-cluster"

        self.__PRODBranch = "master"
        self.__DEVBranch = "DEV"

        self.__launchSecurity = self.__GetLaunchSecurity()

        launchMode = self.__VerifyDBUri()
        if (self.__launchSecurity
            and
            ((launchMode == "DEV") or (launchMode == "PROD"))
        ):
            self.__VerifyBranch(launchMode)
        self.__VerifyDBAccess()


    def __GetLaunchSecurity(self):
        launchSecurity = None
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            launchSecurity = config["Mode"]["launchSecurity"]
        if ((launchSecurity is None) or (type(launchSecurity) is not bool)):
            raise ValueError("FATAL ERROR: INVALID CONFIG")
        return launchSecurity


    # Verify the DB Uri
    def __VerifyDBUri(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        launchMode = self.__GetLaunchMode()
        if (launchMode != self.__EvaluateDBUri()):
            raise ValueError("FATAL ERROR: INVALID LAUNCH MODE")
        return launchMode


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


    # Veify the current launching branch
    def __VerifyBranch(self, launchMode: str):
        branchName = self.__GetBranchName()
        if ((launchMode == "DEV") and (branchName == self.__DEVBranch)):
            return
        if ((launchMode == "PROD") and (branchName == self.__PRODBranch)):
            return
        raise ValueError("FATAL ERROR: ILLEGAL LAUNCH")


    def __GetBranchName(self):
        Repo = Repository(".")
        HEAD = Repo.lookup_reference('HEAD').resolve()
        branchName = HEAD.name
        return branchName.replace("refs/heads/", "")


    # Verify that the current machine is allowed to run Magi
    def __VerifyDBAccess(self):
        try:
            client = pymongo.MongoClient(os.getenv("DB_URI"))
            client.admin.command('ping')
        except:
            raise ValueError("FATAL ERROR: YOU ARE NOT ALLOWED TO LAUNCH THE SERVER BY YOURSELF")
