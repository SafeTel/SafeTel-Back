##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## WhiteListDB
##

# Client mongo db import
import pymongo

# Import db name
from config import dbname

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# Not found definition
NOT_FOUND = 404

# Object to represent table Whitelist
class WhitelistDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Whitelist = self.db['Whitelist']

    def newWhitelist(self, guid):
        data = {
            "guid": guid,
            "PhoneNumbers": []
        }
        self.Whitelist.insert_one(data)

    def deleteWhitelist(self, guid):
        self.Whitelist.delete_one({'guid': guid})

    def exists(self, guid):
        result = self.Whitelist.find_one({'guid': guid})
        return True if result is not None else False

    def getWhitelistForUser(self, id):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return NOT_FOUND
        return result

    def addWhitelistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.append(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Whitelist.update_one(query, query_values)

    def delWhitelistNumberForUser(self, id, number):
        query = {
            'userId': str(id)
        }
        result = self.Whitelist.find_one(query)
        if result is None:
            return
        updated_values = result["phoneNumbers"]
        updated_values.remove(number)
        query_values = { "$set": { 'phoneNumbers': updated_values } }
        self.Whitelist.update_one(query, query_values)
