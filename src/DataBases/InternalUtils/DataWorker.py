##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DataWorker
##

# Client mongo db import
import pymongo

# Create a document linked in MongoDb
def InsertDocument(db, data):
    if data == None:
        return
    db.insert_one(data)

# Delete a document linked to a guid in MongoDb
def DeleteDocument(db, guid):
    if guid == None:
        return
    db.delete_one(guid)
