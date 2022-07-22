##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Balthasar
##

### LOGIC
# For logging
import logging
# For Getenv
import os

class Balthasar():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize
        self.__Filepath = filepath

        if client is None:
            raise Exception("Client is None")
        self.__BalthasarName = os.getenv("DB_BALTHASAR")
        self.__BalthasarDB = client[self.__BalthasarName]

        if self.__BalthasarDB is None:
            raise Exception("BalthasarDB is None")
        self.__Save()

    def __Save(self):
        # Balthasar mongoDB Saving
        Boxes = self.__BalthasarDB['Boxes']
        if (Boxes is None):
            raise Exception("Boxes Collection is None")
        # GetCollectionContentAndFunc(Boxes, )

        UnclaimedBoxes = self.__BalthasarDB['UnclaimedBoxes']
        if (UnclaimedBoxes is None):
            raise Exception("UnclaimedBoxes Collection is None")
        # GetCollectionContentAndFunc(UnclaimedBoxes, )
