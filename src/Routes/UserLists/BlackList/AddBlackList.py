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
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.BlackListDB import BlacklistDB

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
            return BadRequestError("bad request"), 400, 400

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        guid = data['guid']
        BlacklistDb.addBlacklistNumberForUser(guid, body["number"])
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
