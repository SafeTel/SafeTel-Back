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
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Validate Body for AddBlackList route
def ULDelWhiteListListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Route to del a number to the whitelist of the user
class DelWhiteList(Resource):
    def delete(self):
        body = fquest.get_json()
        if not ULDelWhiteListListValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        guid = data['guid']
        number = body["number"]
        WhitelistDb.delWhitelistNumberForUser(guid, number)
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200

