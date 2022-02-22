##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DelWhiteList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

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
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        WhitelistDb.delWhitelistNumberForUser(guid, number)
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200
