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


    def AddNumberFromList(self, guid, number):
        query = {
            'guid': str(guid)
        }
        result = self.DB.find_one(query)
        if result is None:
            return
        updated_values = result["PhoneNumbers"]
        updated_values.append(number)
        query_values = { "$set": { 'PhoneNumbers': updated_values } }
        self.DB.update_one(query, query_values)


    def DeleteNumberFromList(self, guid, number):
        query = {
            'guid': str(guid)
        }
        result = self.DB.find_one(query)
        if result is None:
            return
        updated_values = result["PhoneNumbers"]
        updated_values.remove(number)
        query_values = { "$set": { 'PhoneNumbers': updated_values } }
        self.DB.update_one(query, query_values)
