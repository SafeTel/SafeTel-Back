##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## DataWorker
##

# Client mongo db import
import pymongo

def AddNumberToPhoneList(db, guid, number):
    query = {
        'guid': str(guid)
    }
    result = db.find_one(query)
    if result is None:
        return
    updated_values = result["PhoneNumbers"]
    updated_values.append(number)
    query_values = { "$set": { 'PhoneNumbers': updated_values } }
    db.update_one(query, query_values)

def DeleteNumberFromPhoneList(db, guid, number):
    query = {
        'guid': str(guid)
    }
    result = db.find_one(query)
    if result is None:
        return
    updated_values = result["PhoneNumbers"]
    updated_values.remove(number)
    query_values = { "$set": { 'PhoneNumbers': updated_values } }
    db.update_one(query, query_values)

def UpdateAccountEmail(db, guid, email):
    query = {
        'guid': str(guid)
    }
    result = db.find_one(query)
    if result is None:
        return
    query_values = { "$set": { 'email': email } }
    db.update_one(query, query_values)

def GetAccountsByRole(db, roleTarget):
    query = {
        'role': roleTarget
    }
    return db.find(query)
