##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Casper
##

### LOGIC
# For Logging
import logging
# For Getenv
import os

### INFRA
# For File logging
from Collections.FileLogger import FileLogger
# Utils for saving
from Collections.Utils import GetCollectionContentAndFunc

class Casper():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, filepath):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize
        self.__Filepath = filepath

        if client is None:
            raise Exception("Client is None")
        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperDB = client[self.__CasperName]

        if self.__CasperDB is None:
            raise Exception("CasperDB is None")
        self.__InitLogger()
        self.__Save()

    def __InitLogger(self):
        self.__Logger = FileLogger("CasperLogger", self.__Filepath+"/Casper", "")

    def __Save(self):
        self.__SaveApiKeyLog()
        self.__SaveContributors()

    def __SaveApiKeyLog(self):
        self.__Logger.UpdateFileHandlerFileName("/ApiKeyLog.json")

        ApiKeyLog = self.__CasperDB['ApiKeyLog']
        if (ApiKeyLog is None):
            raise Exception("ApiKeyLog Collection is None")
        logging.info("Save Casper ApiKeyLog")
        GetCollectionContentAndFunc(ApiKeyLog, self.__Logger.LoggingBsonIntoJson)

    def __SaveContributors(self):
        self.__Logger.UpdateFileHandlerFileName("/Contributors.json")

        Contributors = self.__CasperDB['Contributors']
        if (Contributors is None):
            raise Exception("Contributors Collection is None")
        logging.info("Save Casper Contributors")
        GetCollectionContentAndFunc(Contributors, self.__Logger.LoggingBsonIntoJson)
