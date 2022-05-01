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
from pathlib import Path
from pickle import FALSE, TRUE

### INFRA
# Client mongo db import
import pymongo
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class InitLocalServer():
    def __init__(self):
        isLocal = self.__LaunchCheck()
        if not isLocal:
            logging.warning("LaunchMode not Local. Cancelling Local Server Configuration")
            return

        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentMaxValue = 5000000000 # 5 billions
        self.__DocumentPageSize = 50


        logging.warning("Env Vars")
        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__BalthasarName = os.getenv("DB_BALTHASAR")

        self.__MongoDBClientToCopy = None
        self.__MongoDBClient = None
        logging.warning("Generating Clients")
        self.__GenerateClients()

        self.__CopyDataFromServer()


    def __LaunchCheck(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            launchMode = config["Mode"]["launchMode"]
            if (launchMode != "LOCAL"):
                return False
            return True

    def __CopyDataFromServer(self):
        logging.warning("Copying")
        if self.__MongoDBClientToCopy is None or self.__MongoDBClient is None:
            raise Exception("MongoDB Clients None")
        logging.warning(">! Starting")
        self.__MelchiorCopy()
        logging.warning(">!\t __MelchiorCopy Done")
        self.__CasperCopy()
        logging.warning(">!\t __CasperCopy Done")
        self.__CasperTwoCopy()
        logging.warning(">!\t __CasperTwoCopy Done")
        self.__BalthasarCopy()
        logging.warning(">!\t __BalthasarCopy Done")

    def __MelchiorCopy(self):
        # Melchior mongoDB Copy
        Melchior = self.__MongoDBClient[self.__MelchiorName]
        MelchiorToCopy =  self.__MongoDBClientToCopy[self.__MelchiorName]
        Blacklist = Melchior['Blacklist']
        History = Melchior['History']
        User = Melchior['User']
        Whitelist = Melchior['Whitelist']
        BlacklistToCopy = MelchiorToCopy['Blacklist']
        HistoryToCopy = MelchiorToCopy['History']
        UserToCopy = MelchiorToCopy['User']
        WhitelistToCopy = MelchiorToCopy['Whitelist']

        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            BlacklistDocumentsWithPagingInList = list(BlacklistToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(BlacklistDocumentsWithPagingInList) <= 0:
                break
            Blacklist.insert_many(BlacklistDocumentsWithPagingInList)

        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            HistoryDocumentsWithPagingInList = list(HistoryToCopy.find().skip(RangeMin).limit(RangeMax))

            logging.warning(HistoryDocumentsWithPagingInList)
            if len(list(HistoryDocumentsWithPagingInList)) <= 0:
                break
            History.insert_many(list(HistoryDocumentsWithPagingInList))

        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            UserDocumentsWithPagingInList = list(UserToCopy.find().skip(RangeMin).limit(RangeMax))
            
            logging.warning(UserDocumentsWithPagingInList)
            if len(list(UserDocumentsWithPagingInList)) <= 0:
                break
            User.insert_many(list(UserDocumentsWithPagingInList))

        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            WhitelistDocumentsWithPagingInList = list(WhitelistToCopy.find().skip(RangeMin).limit(RangeMax))
            
            logging.warning(WhitelistDocumentsWithPagingInList)
            if len(list(WhitelistDocumentsWithPagingInList)) <= 0:
                break
            Whitelist.insert_many(list(WhitelistDocumentsWithPagingInList))

    def __CasperCopy(self):
        # Casper mongoDB Copy
        Casper = self.__MongoDBClient[self.__CasperName]
        CasperToCopy =  self.__MongoDBClientToCopy[self.__CasperName]
        ApiKeyLog = Casper['ApiKeyLog']
        Contributors = Casper['Contributors']
        ApiKeyLogToCopy = CasperToCopy['ApiKeyLog']
        ContributorsToCopy = CasperToCopy['Contributors']

        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            ApiKeyLogDocumentsWithPagingInList = list(ApiKeyLogToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(ApiKeyLogDocumentsWithPagingInList)) <= 0:
                break
            ApiKeyLog.insert_many(list(ApiKeyLogDocumentsWithPagingInList))

        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
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
        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            GoogleServicesDocumentsWithPagingInList = list(GoogleServicesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(GoogleServicesDocumentsWithPagingInList)) <= 0:
                break
            GoogleServices.insert_many(list(GoogleServicesDocumentsWithPagingInList))

    def __BalthasarCopy(self):
        # Balthasar mongoDB Copy
        Balthasar = self.__MongoDBClient[self.__BalthasarName]
        BalthasarToCopy =  self.__MongoDBClientToCopy[self.__BalthasarName]
        Boxes = Balthasar['Boxes']
        UnclaimedBoxes = Balthasar['UnclaimedBoxes']
        BoxesToCopy = BalthasarToCopy['Boxes']
        UnclaimedBoxesToCopy = BalthasarToCopy['UnclaimedBoxes']

        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
            BoxesDocumentsWithPagingInList = list(BoxesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(BoxesDocumentsWithPagingInList)) <= 0:
                break
            Boxes.insert_many(list(BoxesDocumentsWithPagingInList))

        for i in range(self.__DocumentMaxValue): 
            RangeMin = i * self.__DocumentPageSize
            RangeMax = self.__DocumentPageSize + RangeMin
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
        logging.warning("Clients generated")
        return True, "Safetel mongoDB available"
