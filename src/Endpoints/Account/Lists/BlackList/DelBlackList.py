##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DelBlackList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

# Validate Body for DelBlackList route
def ULDelBlackListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Route to delete a number to the blacklist of the user
class DelBlackList(Resource):
    def delete(self):
        body = fquest.get_json()
        if not ULDelBlackListValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        BlacklistDb.delBlacklistNumberForUser(guid, number)
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
