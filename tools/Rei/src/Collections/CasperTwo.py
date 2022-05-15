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
        self.__CasperTwoDBToCopy = clientToCopy[self.__CasperTwoName]
        if self.__CasperTwoDB is None:
            raise Exception("CasperTwoDB is None")
        if self.__CasperTwoDBToCopy is None:
            raise Exception("CasperTwoDBToCopy is None")
        self.__Copy()

    def __Copy(self):
        # CasperTwo mongoDB Copy

        GoogleServices = self.__CasperTwoDB['GoogleServices']
        GoogleServicesToCopy = self.__CasperTwoDBToCopy['GoogleServices']
        if (GoogleServices is None or GoogleServicesToCopy is None):
            raise Exception("GoogleServices Collection is None")
        CopyAndUpload(GoogleServicesToCopy, GoogleServices)
