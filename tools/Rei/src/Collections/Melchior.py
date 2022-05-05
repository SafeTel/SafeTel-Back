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
# Utils for uploading
from Collections.Utils import CopyAndUpload

class Melchior():
    def __init__(self, DocumentsMaxIterationNumber, DocumentsPageSize, client, clientToCopy):
        # Using i for paging datas -> avoiding the use of to much memory at the same time
        self.__DocumentsMaxIterationNumber = DocumentsMaxIterationNumber # 5 billions
        self.__DocumentsPageSize = DocumentsPageSize

        if client is None:
            raise Exception("Client is None")
        self.__MelchiorName = os.getenv("DB_MELCHIOR")
        self.__MelchiorDB = client[self.__MelchiorName]
        self.__MelchiorDBToCopy = clientToCopy[self.__MelchiorName]

        if self.__MelchiorDB is None:
            raise Exception("MelchiorDB is None")
        if self.__MelchiorDBToCopy is None:
            raise Exception("MelchiorDBToCopy is None")
        self.__Copy()

    def __Copy(self):
        # Melchior mongoDB Copy
        Blacklist = self.__MelchiorDB['Blacklist']
        BlacklistToCopy = self.__MelchiorDBToCopy['Blacklist']
        if (Blacklist is None or BlacklistToCopy is None):
            raise Exception("Blacklist Collection is None")
        CopyAndUpload(BlacklistToCopy, Blacklist)

        History = self.__MelchiorDB['History']
        HistoryToCopy = self.__MelchiorDBToCopy['History']
        if (History is None or HistoryToCopy is None):
            raise Exception("History Collection is None")
        CopyAndUpload(HistoryToCopy, History)

        User = self.__MelchiorDB['User']
        UserToCopy = self.__MelchiorDBToCopy['User']
        if (User is None or UserToCopy is None):
            raise Exception("User Collection is None")
        CopyAndUpload(UserToCopy, User)

        Whitelist = self.__MelchiorDB['Whitelist']
        WhitelistToCopy = self.__MelchiorDBToCopy['Whitelist']

        if (Whitelist is None or WhitelistToCopy is None):
            raise Exception("Whitelist Collection is None")
        CopyAndUpload(WhitelistToCopy, Whitelist)
