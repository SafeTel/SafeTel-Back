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
# To perform Ping
import requests

# Class to perform Copy
from Collections.Melchior import Melchior
from Collections.Casper import Casper
from Collections.CasperTwo import CasperTwo
from Collections.Balthasar import Balthasar

class ConfigDatabase():
    def __init__(self):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = 5000000000 # 5 billions
        self.__DocumentsPageSize = 50

        self.__MongoDBClientToCopy = None
        self.__MongoDBClient = None
        err, msg = self.__GenerateClients()

        if err == False:
            logging.warning(msg)
            return
        self.__CopyDataFromServer()

    def __CopyDataFromServer(self):
        if self.__MongoDBClientToCopy is None or self.__MongoDBClient is None:
            raise Exception("MongoDB Clients None")
        Melchior(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__MongoDBClientToCopy)
        Casper(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__MongoDBClientToCopy)
        CasperTwo(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__MongoDBClientToCopy)
        Balthasar(self.__DocumentsMaxIterationNumber, self.__DocumentsPageSize, self.__MongoDBClient, self.__MongoDBClientToCopy)

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
