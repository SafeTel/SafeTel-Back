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
# Utils for uploading
from Collections.Utils import CopyAndUpload

class Balthasar():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__BalthasarName = os.getenv("DB_BALTHASAR")
        self.__BalthasarDB = client[self.__BalthasarName]
        self.__BalthasarDBToCopy = clientToCopy[self.__BalthasarName]

        if self.__BalthasarDB is None:
            raise Exception("BalthasarDB is None")
        if self.__BalthasarDBToCopy is None:
            raise Exception("BalthasarDBToCopy is None")
        self.__Copy()

    def __Copy(self):
        # Balthasar mongoDB Copy
        Boxes = self.__BalthasarDB['Boxes']
        BoxesToCopy = self.__BalthasarDBToCopy['Boxes']
        if (Boxes is None or BoxesToCopy is None):
            raise Exception("Boxes Collection is None")
        CopyAndUpload(BoxesToCopy, Boxes)

        UnclaimedBoxes = self.__BalthasarDB['UnclaimedBoxes']
        UnclaimedBoxesToCopy = self.__BalthasarDBToCopy['UnclaimedBoxes']
        if (UnclaimedBoxes is None or UnclaimedBoxesToCopy is None):
            raise Exception("UnclaimedBoxes Collection is None")
        CopyAndUpload(UnclaimedBoxesToCopy, UnclaimedBoxes)