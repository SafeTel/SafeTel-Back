##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UserDBWorker
##

### INFRA
# mongodb import
import pymongo

class UserDBWorker():
    def __init__(self, db):
        self.DB = db


    def ChangeToLostPasswordMode(self, guid: str, mode: bool):
        query = { 'guid': str(guid) }
        result = self.DB.find_one(query)
        if result is None:
            return
        query_values = { "$set": { "Administrative.passwordlost": mode } }
        self.DB.update_one(query, query_values)


    def UpdateLostPassword(self, guid: str, newpassword: str):
        query = { 'guid': str(guid) }
        result = self.DB.find_one(query)
        if result is None:
            return
        query_values = { "$set": { "password": newpassword } }
        self.DB.update_one(query, query_values)


    def UpdateAccountEmail(self, guid: str, email: str):
        query = { 'guid': str(guid)}
        result = self.DB.find_one(query)
        if result is None:
            return
        query_values = { "$set": { "email": email } }
        self.DB.update_one(query, query_values)


    def UpdatePersonalInfos(self, guid: str, customerInfos: dict, localization: dict):
        query = {'guid': str(guid)}
        result = self.DB.find_one(query)
        if result is None:
            return
        query_values = { "$set": { "CustomerInfos": customerInfos } }
        self.DB.update_one(query, query_values)
        query_values = { "$set": { "Localization": localization } }
        self.DB.update_one(query, query_values)
