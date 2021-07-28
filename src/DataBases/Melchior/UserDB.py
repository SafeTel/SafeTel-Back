##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## UserDB
##

# Client mongo db import
import pymongo

# Import db name
from config import dbname

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# Object to represent table User
class UserDB():
    def __init__(self, db_name=dbname):
        self.client = pymongo.MongoClient(URI_MELCHIOR)
        self.db = self.client[db_name]
        self.Users = self.db['User']

    def addUser(self, user_data):
        self.Users.insert_one(user_data)

    def deleteUser(self, guid):
        self.Users.delete_one({'guid': guid})

    def exists(self, email):
        result = self.Users.find_one({'email': email})
        return True if result is not None else False

    def getUser(self, email):
        result = self.Users.find_one({'email': email})
        return result

    def getUserByGUID(self, guid):
        result = self.Users.find_one({'guid': guid})
        return result
