##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## AddBlackList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Endpoints.Utils.Request import validateBody
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

# Validate Body for AddBlackList route
def ULAddBlackListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Route to add a number to the blacklist of the user
class AddBlackList(Resource):
    def post(self):
        body = fquest.get_json()
        if not ULAddBlackListValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        BlacklistDb.addBlacklistNumberForUser(guid, body["number"])
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
