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
from Routes.Utils.JWTProvider.Provider import DeserializeJWT

# DB import
from DataBases.Melchior.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

class AddBlackList(Resource):
    def post(self):
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
        BlacklistDb.addBlacklistNumberForUser(guid, body["number"])
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
