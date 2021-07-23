##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## AddBlackList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody

# DB import
from DataBases.Melchior import BlacklistDB

BlacklistDb = BlacklistDB()

class AddBlackList(Resource):
    def post(self):
        if not validateBody(fquest.get_json(), ["userId", "number"]):
            return {
                'error': 'bad_request'
            }, 400
        body = fquest.get_json()
        userId = body["userId"]
        number = body["number"]
        BlacklistDb.addBlacklistNumberForUser(userId, number)
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(userId)["phoneNumbers"]
        }, 200
