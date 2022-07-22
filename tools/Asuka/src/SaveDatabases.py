##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## config
##

### LOGIC
import logging
# For Getenv
import os
# Load json
import json

### INFRA
# Client mongo db import
import pymongo
# Class to perform Copy
from Collections.Melchior import Melchior
from Collections.Casper import Casper
from Collections.CasperTwo import CasperTwo
from Collections.Balthasar import Balthasar
from Collections.BalthasarTwo import BalthasarTwo
# Class to init parameters
from InitSaveFileParameters import InitSaveFileParameters

class SaveDatabases():
    def __init__(self):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = 5000000000 # 5 billions
        self.__DocumentsPageSize = 50

        self.__MongoDBClient = None
        err, msg = self.__GenerateClients()

        if (err == False):
            raise Exception(msg)            
        elif (self.__MongoDBClient is None):
            raise Exception("MongoDB Clients None")
        self.__SaveFileParameters = InitSaveFileParameters()
        self.__SaveDataFromServer()

    def __SaveDataFromServer(self):
        Melchior(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__SaveFileParameters.GetFilePath())
        Casper(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__SaveFileParameters.GetFilePath())
        CasperTwo(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__SaveFileParameters.GetFilePath())
        Balthasar(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__SaveFileParameters.GetFilePath())
        BalthasarTwo(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__SaveFileParameters.GetFilePath())

    def __GenerateClients(self):
        try:
            uri = os.getenv("DB_URI")
            client = pymongo.MongoClient(uri)
            self.__MongoDBClient = client

        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, "Safetel mongoDB available"
