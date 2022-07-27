##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BalthasarTwo
##

### LOGIC
# For Logging
import logging
# For Getenv
import os

### INFRA
# For File logging
from Collections.FileLogger import FileLogger
# Utils for saving
from Collections.Utils import GetCollectionContentAndFunc

class BalthasarTwo():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, filepath):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize
        self.__Filepath = filepath

        if client is None:
            raise Exception("Client is None")
        self.__BalthasarTwoName = os.getenv("DB_BALTHASAR_02")
        self.__BalthasarTwoDB = client[self.__BalthasarTwoName]

        if self.__BalthasarTwoDB is None:
            raise Exception("BalthasarDB is None")
        self.__InitLogger()
        self.__Save()

    def __InitLogger(self):
        self.__Logger = FileLogger("BalthasarTwoLogger", self.__Filepath+"/BalthaserTwo", "")

    def __Save(self):
        self.__Logger.UpdateFileHandlerFileName("/Fr_0033.json")

        Fr_0033 = self.__BalthasarTwoDB['FR-0033']
        if (Fr_0033 is None):
            raise Exception("Fr_0033 Collection is None")
        logging.info("Save BalthasarTwo FR-0033")
        GetCollectionContentAndFunc(Fr_0033, self.__Logger.LoggingBsonIntoJson)
