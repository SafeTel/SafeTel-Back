##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UserDBWatcher
##

### INFRA
# mongodb import
import pymongo

class UserDBWatcher():
    def __init__(self, db):
        self.DB = db


    def GetAccountsByRole(self, roleTarget):
        query = {
            'role': roleTarget
        }
        return self.DB.find(query)
