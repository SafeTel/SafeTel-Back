##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## DataWorker
##

### INFRA
# mongodb import
import pymongo

class UserListsWorker():
    def __init__(self, db):
        self.DB = db


    ### PUBLIC

    def AddNumberFromList(self, guid, number):
        CurrentList = self.__PullList(guid)
        if (CurrentList is None):
            return
        NewList = self.__AddNumber(number, CurrentList["PhoneNumbers"])
        self.__UpdateList(guid, NewList)


    def DeleteNumberFromList(self, guid: str, number: str):
        CurrentList = self.__PullList(guid)
        if (CurrentList is None):
            return
        NewList = self.__DeleteNumber(number, CurrentList["PhoneNumbers"])
        self.__UpdateList(guid, NewList)


    ### PRIVATE

    def __PullList(self, guid):
        query = {
            'guid': str(guid)
        }
        return self.DB.find_one(query)


    def __UpdateList(self, guid: str, List: list):
        query = {
            'guid': str(guid)
        }
        query_values = { "$set": {
                'PhoneNumbers': List
            }
        }
        self.DB.update_one(query, query_values)


    def __AddNumber(self, number: str, TemporaryList: list):
        if (not self.__IsNumberInList(number, TemporaryList)):
            TemporaryList.append(number)
        return TemporaryList


    def __DeleteNumber(self, number: str, TemporaryList: list):
        if (self.__IsNumberInList(number, TemporaryList)):
            TemporaryList.remove(number)
        return TemporaryList


    def __IsNumberInList(self, targetnumber: str, Numbers: list):
        if (targetnumber in Numbers):
                return True
        return False
