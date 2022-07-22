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

from Collections.FileLogger import FileLogger

from Collections.Utils import GetCollectionContentAndFunc

class Balthasar():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, filepath):
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
        logger = FileLogger("BalthaserBoxesLogger", self.__Filepath, "/Boxes.json")
        # Balthasar mongoDB Saving
        Boxes = self.__BalthasarDB['Boxes']
        if (Boxes is None):
            raise Exception("Boxes Collection is None")
        logging.info("Save Balthasar Boxes")

        GetCollectionContentAndFunc(Boxes, logger.LoggingList)

        UnclaimedBoxes = self.__BalthasarDB['UnclaimedBoxes']
        if (UnclaimedBoxes is None):
            raise Exception("UnclaimedBoxes Collection is None")
        logging.info("Save Balthasar UnclaimedBoxes")
        # GetCollectionContentAndFunc(UnclaimedBoxes, )
