##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Melchior
##

### LOGIC
# For Getenv
import logging
import os

class Melchior():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__MelchiorDB = client[self.__MelchiorName]
        self.__MelchiorDBToCopy = clientToCopy[self.__MelchiorName]
        self.__Copy()

    def __Copy(self):
        # Melchior mongoDB Copy
        Blacklist = self.__MelchiorDB['Blacklist']
        BlacklistToCopy = self.__MelchiorDBToCopy['Blacklist']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            BlacklistDocumentsWithPagingInList = list(BlacklistToCopy.find().skip(RangeMin).limit(RangeMax))


            if len(BlacklistDocumentsWithPagingInList) <= 0:
                break
            Blacklist.insert_many(BlacklistDocumentsWithPagingInList)

        History = self.__MelchiorDB['History']
        HistoryToCopy = self.__MelchiorDBToCopy['History']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            HistoryDocumentsWithPagingInList = list(HistoryToCopy.find().skip(RangeMin).limit(RangeMax))

            if len(list(HistoryDocumentsWithPagingInList)) <= 0:
                break
            History.insert_many(list(HistoryDocumentsWithPagingInList))

        User = self.__MelchiorDB['User']
        UserToCopy = self.__MelchiorDBToCopy['User']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            UserDocumentsWithPagingInList = list(UserToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(UserDocumentsWithPagingInList)) <= 0:
                break
            User.insert_many(list(UserDocumentsWithPagingInList))

        Whitelist = self.__MelchiorDB['Whitelist']
        WhitelistToCopy = self.__MelchiorDBToCopy['Whitelist']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            WhitelistDocumentsWithPagingInList = list(WhitelistToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(WhitelistDocumentsWithPagingInList)) <= 0:
                break
            Whitelist.insert_many(list(WhitelistDocumentsWithPagingInList))
