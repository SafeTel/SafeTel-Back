##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## BlackListDB
##

# Client mongo db import
import pymongo

# Import db name
from config import dbname

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# Not found definition
NOT_FOUND = 404

# Object to represent table Blacklist
class BlacklistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Blacklist = self.db['Blacklist']

    def newBlacklist(self, guid):
        data = {
            "guid": guid,
            "PhoneNumbers": []
        }
        self.Blacklist.insert_one(data)

    def deleteBlacklist(self, guid):
        self.Blacklist.delete_one({'guid': guid})

    def exists(self, guid):
        result = self.Blacklist.find_one({'guid': guid})
        return True if result is not None else False

    def getBlacklistForUser(self, id):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return NOT_FOUND
        return result

    def addBlacklistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.append(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Blacklist.update_one(query, query_values)

    def delBlacklistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Blacklist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.remove(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Blacklist.update_one(query, query_values)
