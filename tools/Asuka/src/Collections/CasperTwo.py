##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## CasperTwo
##

### LOGIC
# For Getenv
import logging
import os
# Utils for uploading
from Collections.Utils import CopyAndUpload

class CasperTwo():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__CasperTwoDB = client[self.__CasperTwoName]
        if self.__CasperTwoDB is None:
            raise Exception("CasperTwoDB is None")
        self.__Save()

    def __Save(self):
        # CasperTwo mongoDB Save
        GoogleServices = self.__CasperTwoDB['GoogleServices']
        if (GoogleServices is None):
            raise Exception("GoogleServices Collection is None")
        logging.info("Save CasperTwo GoogleServices")
        # GetCollectionContentAndFunc(GoogleServices, )
