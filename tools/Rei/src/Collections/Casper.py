##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Casper
##

### LOGIC
# For Getenv
import logging
import os
# Utils for uploading
from Collections.Utils import CopyAndUpload

class Casper():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperDB = client[self.__CasperName]
        self.__CasperDBToCopy = clientToCopy[self.__CasperName]

        if self.__CasperDB is None:
            raise Exception("CasperDB is None")
        if self.__CasperDBToCopy is None:
            raise Exception("CasperDBToCopy is None")
        self.__Copy()

    def __Copy(self):
        # Casper mongoDB Copy

        ApiKeyLog = self.__CasperDB['ApiKeyLog']
        ApiKeyLogToCopy = self.__CasperDBToCopy['ApiKeyLog']
        if (ApiKeyLog is None or ApiKeyLogToCopy is None):
            raise Exception("ApiKeyLog Collection is None")
        CopyAndUpload(ApiKeyLogToCopy, ApiKeyLog)

        Contributors = self.__CasperDB['Contributors']
        ContributorsToCopy = self.__CasperDBToCopy['Contributors']
        if (Contributors is None or ContributorsToCopy is None):
            raise Exception("Contributors Collection is None")
        CopyAndUpload(ContributorsToCopy, Contributors)
