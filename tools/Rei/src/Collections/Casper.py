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

class Casper():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        self.__CasperName = os.getenv("DB_CASPER")
        self.__CasperDB = client[self.__CasperName]
        self.__CasperDBToCopy = clientToCopy[self.__CasperName]
        self.__Copy()

    def __Copy(self):
        # Casper mongoDB Copy

        ApiKeyLog = self.__CasperDB['ApiKeyLog']
        ApiKeyLogToCopy = self.__CasperDBToCopy['ApiKeyLog']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            ApiKeyLogDocumentsWithPagingInList = list(ApiKeyLogToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(ApiKeyLogDocumentsWithPagingInList)) <= 0:
                break
            ApiKeyLog.insert_many(list(ApiKeyLogDocumentsWithPagingInList))

        Contributors = self.__CasperDB['Contributors']
        ContributorsToCopy = self.__CasperDBToCopy['Contributors']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            ContributorsDocumentsWithPagingInList = list(ContributorsToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(ContributorsDocumentsWithPagingInList)) <= 0:
                break
            Contributors.insert_many(list(ContributorsDocumentsWithPagingInList))