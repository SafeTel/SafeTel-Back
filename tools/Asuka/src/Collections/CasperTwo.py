##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## CasperTwo
##

### LOGIC
# For Getenv
import os
# For Logging
import logging

### INFRA
# For File logging
from Collections.FileLogger import FileLogger
# Utils for saving
from Collections.Utils import GetCollectionContentAndFunc

class CasperTwo():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, filepath):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize
        self.__Filepath = filepath

        if (client is None):
            raise Exception("Client is None")
        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__CasperTwoDB = client[self.__CasperTwoName]

        if (self.__CasperTwoDB is None):
            raise Exception("CasperTwoDB is None")
        self.__InitLogger()
        self.__Save()

    def __InitLogger(self):
        self.__Logger = FileLogger("CasperTwoLogger", self.__Filepath+"/CasperTwo", "")

    def __Save(self):
        self.__Logger.UpdateFileHandlerFileName("/GoogleServices.json")

        GoogleServices = self.__CasperTwoDB['GoogleServices']
        if (GoogleServices is None):
            raise Exception("GoogleServices Collection is None")
        logging.info("Save CasperTwo GoogleServices")
        GetCollectionContentAndFunc(GoogleServices, self.__Logger.LoggingBsonIntoJson)
