##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## config
##

### LOGIC
import logging
import os
import json

### INFRA
# Client mongo db import
import pymongo
import requests

class InitDatabase():
    def __init__(self):
        self.__IsValidConfig()
        self.__CheckEnvVars()
        self.__Ping()
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = 5000000000 # 5 billions
        self.__DocumentsPageSize = 50

        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__BalthasarName = os.getenv("DB_BALTHASAR")

        self.__MongoDBClientToCopy = None
        self.__MongoDBClient = None
        err, msg = self.__GenerateClients()

        if err == False:
            logging.warning(msg)
            return
        self.__CopyDataFromServer()

    def __IsValidConfig(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            if ("MandatoryEnvVars" not in config):
                raise ValueError("FATAL ERROR: Configuration Denied")

    def __CheckEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("FATAL ERROR: Environement Denied")

    def __Ping(self):
        pingUri = os.getenv("PING_URI")
        response = requests.get(pingUri)

        if (self.__IsValidResponse(response)):
            raise ValueError("FATAL ERROR: Environement Denied")

    def __IsValidResponse(self, response: requests.Response):
        NominalCode = 200
        NominalHeaders = [
            "text/json; charset=utf-8",
            "text/html; charset=UTF-8"
        ]

        if (response.status_code != NominalCode):
            return False
        for NominalHeader in NominalHeaders:
            if (response.headers == NominalHeader):
                return True
        return False

    def __CopyDataFromServer(self):
        if self.__MongoDBClientToCopy is None or self.__MongoDBClient is None:
            raise Exception("MongoDB Clients None")
        self.__MelchiorCopy()
        self.__CasperCopy()
        self.__CasperTwoCopy()
        self.__BalthasarCopy()

    def __MelchiorCopy(self):
        # Melchior mongoDB Copy
        Melchior = self.__MongoDBClient[self.__MelchiorName]
        MelchiorToCopy =  self.__MongoDBClientToCopy[self.__MelchiorName]

        Blacklist = Melchior['Blacklist']
        BlacklistToCopy = MelchiorToCopy['Blacklist']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            BlacklistDocumentsWithPagingInList = list(BlacklistToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(BlacklistDocumentsWithPagingInList) <= 0:
                break
            Blacklist.insert_many(BlacklistDocumentsWithPagingInList)

        History = Melchior['History']
        HistoryToCopy = MelchiorToCopy['History']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            HistoryDocumentsWithPagingInList = list(HistoryToCopy.find().skip(RangeMin).limit(RangeMax))

            if len(list(HistoryDocumentsWithPagingInList)) <= 0:
                break
            History.insert_many(list(HistoryDocumentsWithPagingInList))

        User = Melchior['User']
        UserToCopy = MelchiorToCopy['User']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            UserDocumentsWithPagingInList = list(UserToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(UserDocumentsWithPagingInList)) <= 0:
                break
            User.insert_many(list(UserDocumentsWithPagingInList))

        Whitelist = Melchior['Whitelist']
        WhitelistToCopy = MelchiorToCopy['Whitelist']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            WhitelistDocumentsWithPagingInList = list(WhitelistToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(WhitelistDocumentsWithPagingInList)) <= 0:
                break
            Whitelist.insert_many(list(WhitelistDocumentsWithPagingInList))

    def __CasperCopy(self):
        # Casper mongoDB Copy
        Casper = self.__MongoDBClient[self.__CasperName]
        CasperToCopy =  self.__MongoDBClientToCopy[self.__CasperName]

        ApiKeyLog = Casper['ApiKeyLog']
        ApiKeyLogToCopy = CasperToCopy['ApiKeyLog']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            ApiKeyLogDocumentsWithPagingInList = list(ApiKeyLogToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(ApiKeyLogDocumentsWithPagingInList)) <= 0:
                break
            ApiKeyLog.insert_many(list(ApiKeyLogDocumentsWithPagingInList))

        Contributors = Casper['Contributors']
        ContributorsToCopy = CasperToCopy['Contributors']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            ContributorsDocumentsWithPagingInList = list(ContributorsToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(ContributorsDocumentsWithPagingInList)) <= 0:
                break
            Contributors.insert_many(list(ContributorsDocumentsWithPagingInList))

    def __CasperTwoCopy(self):
        # CasperTwo mongoDB Copy
        CasperTwo = self.__MongoDBClient[self.__CasperTwoName]
        CasperTwoToCopy =  self.__MongoDBClientToCopy[self.__CasperTwoName]

        GoogleServices = CasperTwo['GoogleServices']
        GoogleServicesToCopy = CasperTwoToCopy['GoogleServices']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            GoogleServicesDocumentsWithPagingInList = list(GoogleServicesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(GoogleServicesDocumentsWithPagingInList)) <= 0:
                break
            GoogleServices.insert_many(list(GoogleServicesDocumentsWithPagingInList))

    def __BalthasarCopy(self):
        # Balthasar mongoDB Copy
        Balthasar = self.__MongoDBClient[self.__BalthasarName]
        BalthasarToCopy =  self.__MongoDBClientToCopy[self.__BalthasarName]

        Boxes = Balthasar['Boxes']
        BoxesToCopy = BalthasarToCopy['Boxes']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            BoxesDocumentsWithPagingInList = list(BoxesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(BoxesDocumentsWithPagingInList)) <= 0:
                break
            Boxes.insert_many(list(BoxesDocumentsWithPagingInList))

        UnclaimedBoxes = Balthasar['UnclaimedBoxes']
        UnclaimedBoxesToCopy = BalthasarToCopy['UnclaimedBoxes']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            UnclaimedBoxesDocumentsWithPagingInList = list(UnclaimedBoxesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(UnclaimedBoxesDocumentsWithPagingInList)) <= 0:
                break
            UnclaimedBoxes.insert_many(list(UnclaimedBoxesDocumentsWithPagingInList))

    def __GenerateClients(self):
        try:
            uri = os.getenv("DB_URI")

            client = pymongo.MongoClient(uri)
            self.__MongoDBClient = client

            uri = os.getenv("DB_URI_SERVER_TO_COPY")
            clientToCopy = pymongo.MongoClient(uri)
            self.__MongoDBClientToCopy = clientToCopy
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, "Safetel mongoDB available"
