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

class CasperTwo():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        self.__CasperTwoName = os.getenv("DB_CASPER_02")
        self.__CasperTwoDB = client[self.__CasperTwoName]
        self.__CasperTwoDBToCopy = clientToCopy[self.__CasperTwoName]
        self.__Copy()

    def __Copy(self):
        # CasperTwo mongoDB Copy

        GoogleServices = self.__CasperTwoDB['GoogleServices']
        GoogleServicesToCopy = self.__CasperTwoDBToCopy['GoogleServices']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            GoogleServicesDocumentsWithPagingInList = list(GoogleServicesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(GoogleServicesDocumentsWithPagingInList)) <= 0:
                break
            GoogleServices.insert_many(list(GoogleServicesDocumentsWithPagingInList))
