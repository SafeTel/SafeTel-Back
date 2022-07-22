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

class Casper():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
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
        self.__Save()

    def __Save(self):
        # Casper mongoDB Saving
        ApiKeyLog = self.__CasperDB['ApiKeyLog']
        if (ApiKeyLog is None):
            raise Exception("ApiKeyLog Collection is None")
        logging.info("Save Casper ApiKeyLog")
        # GetCollectionContentAndFunc(ApiKeyLog, )

        Contributors = self.__CasperDB['Contributors']
        if (Contributors is None):
            raise Exception("Contributors Collection is None")
        logging.info("Save Casper Contributors")
        # GetCollectionContentAndFunc(Contributors, )
