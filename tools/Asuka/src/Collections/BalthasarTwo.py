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

class BalthasarTwo():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__BalthasarTwoName = os.getenv("DB_BALTHASAR_02")
        self.__BalthasarTwoDB = client[self.__BalthasarTwoName]

        if self.__BalthasarTwoDB is None:
            raise Exception("BalthasarDB is None")
        self.__Save()

    def __Save(self):
        # Balthasar mongoDB Saving
        Fr_0033 = self.__BalthasarTwoDB['FR-0033']
        if (Fr_0033 is None):
            raise Exception("Boxes Collection is None")
        logging.info("Save BalthasarTwo FR-0033")
        # GetCollectionContentAndFunc(Fr_0033, )
