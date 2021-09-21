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

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

class DelWhiteList(Resource):
    def delete(self):
        if not validateBody(fquest.get_json(), ["token", "number"]):
            return {
                'error': 'bad_request'
            }, 400
        body = fquest.get_json()

        data = DeserializeJWT(body["token"])
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

