##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Melchior
##

### LOGIC
# For Logging
import logging
# For Getenv
import os

class Melchior():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, filepath):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__MelchiorDB = client[self.__MelchiorName]

        if self.__MelchiorDB is None:
            raise Exception("MelchiorDB is None")
        self.__Save()

    def __Save(self):
        self.__SaveBlacklist()
        self.__SaveHistory()
        self.__SaveUser()
        self.__SaveWhitelist()

    def __SaveBlacklist(self):
        # Melchior mongoDB Save
        Blacklist = self.__MelchiorDB['Blacklist']
        if (Blacklist is None):
            raise Exception("Blacklist Collection is None")
        logging.info("Save Melchior Blacklist")
        # GetCollectionContentAndFunc(Blacklist, )

    def __SaveHistory(self):
        History = self.__MelchiorDB['History']
        if (History is None):
            raise Exception("History Collection is None")
        logging.info("Save Melchior History")
        # GetCollectionContentAndFunc(History, )

    def __SaveUser(self):
        User = self.__MelchiorDB['User']
        if (User is None):
            raise Exception("User Collection is None")
        logging.info("Save Melchior User")
        # GetCollectionContentAndFunc(User, )

    def __SaveWhitelist(self):
        Whitelist = self.__MelchiorDB['Whitelist']

        if (Whitelist is None):
            raise Exception("Whitelist Collection is None")
        logging.info("Save Melchior Whitelist")
        # GetCollectionContentAndFunc(Whitelist, )
