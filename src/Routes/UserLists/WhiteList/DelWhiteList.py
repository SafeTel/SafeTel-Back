##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DelWhiteList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

class DelWhiteList(Resource):
    def delete(self):
        if not validateBody(fquest.get_json(), ["userId", "number"]):
            return {
                'error': 'bad_request'
            }, 400
        body = fquest.get_json()
        userId = body["userId"]
        number = body["number"]
        WhitelistDb.delWhitelistNumberForUser(userId, number)
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(userId)["PhoneNumbers"]
        }, 200

