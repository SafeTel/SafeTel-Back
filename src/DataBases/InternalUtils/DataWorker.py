##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DataWorker
##

# Client mongo db import
import pymongo

def InsertDocument(db, data):
    db.insert_one(data)

def DeleteDocument(db, data):
    db.delete_one(data)
