##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetWhiteList
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# Utils import
from Routes.Utils.JWTProvider.Provider import DeserializeJWT

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

class GetWhiteList(Resource):
    def get(self):
        data = DeserializeJWT(request.args["token"])
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        guid = data['guid']
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200
