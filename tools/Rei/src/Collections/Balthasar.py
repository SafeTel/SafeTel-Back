##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Balthasar
##

### LOGIC
# For Getenv
import logging
import os

class Balthasar():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        self.__BalthasarName = os.getenv("DB_BALTHASAR")
        self.__BalthasarDB = client[self.__BalthasarName]
        self.__BalthasarDBToCopy = clientToCopy[self.__BalthasarName]
        self.__Copy()

    def __Copy(self):
        # Balthasar mongoDB Copy

        Boxes = self.__BalthasarDB['Boxes']
        BoxesToCopy = self.__BalthasarDBToCopy['Boxes']
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            BoxesDocumentsWithPagingInList = list(BoxesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(BoxesDocumentsWithPagingInList)) <= 0:
                break
            Boxes.insert_many(list(BoxesDocumentsWithPagingInList))

        UnclaimedBoxes = self.__BalthasarDB['UnclaimedBoxes']
        UnclaimedBoxesToCopy = self.__BalthasarDBToCopy['UnclaimedBoxes']
        for i in range(self.__DocumentsMaxIterationNumber): 
            RangeMin = i * self.__DocumentsPageSize
            RangeMax = self.__DocumentsPageSize + RangeMin
            UnclaimedBoxesDocumentsWithPagingInList = list(UnclaimedBoxesToCopy.find().skip(RangeMin).limit(RangeMax))
            
            if len(list(UnclaimedBoxesDocumentsWithPagingInList)) <= 0:
                break
            UnclaimedBoxes.insert_many(list(UnclaimedBoxesDocumentsWithPagingInList))