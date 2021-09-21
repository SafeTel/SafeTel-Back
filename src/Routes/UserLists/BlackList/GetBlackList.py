##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetBlackList
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# Utils import
from Routes.Utils.JWTProvider.Provider import DeserializeJWT

# DB import
from DataBases.Melchior.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

class GetBlackList(Resource):
    def get(self):
        data = DeserializeJWT(request.args["token"])
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        guid = data['guid']
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
