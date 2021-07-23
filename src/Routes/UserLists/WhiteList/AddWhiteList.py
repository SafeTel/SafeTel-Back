##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## AddWhiteList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody

# DB import
from DataBases.Melchior import WhitelistDB

WhitelistDb = WhitelistDB()

class AddWhiteList(Resource):
    def post(self):
        if not validateBody(fquest.get_json(), ["userId", "number"]):
            return {
                'error': 'bad_request'
            }, 400
        body = fquest.get_json()
        userId = body["userId"]
        number = body["number"]
        WhitelistDb.addWhitelistNumberForUser(userId, number)
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(userId)["phoneNumbers"]
        }, 200
