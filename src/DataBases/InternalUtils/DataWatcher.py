##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DataWatcher
##

# Client mongo db import
import pymongo

# Not found definition
NOT_FOUND = 404

# Look for a document by giving the db, a query, and data to compare
def GetDocument(db, query, data):
    query_mongo = {
        query: data
    }
    result = db.find_one(query_mongo)
    return result

# Look for a document by giving the db, a query, and data to compare
def IsDocument(db, query, data):
    query_mongo = {
        query: data
    }
    result = db.find_one(query_mongo)
    return True if result is not None else False
