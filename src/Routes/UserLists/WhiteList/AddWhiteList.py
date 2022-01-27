##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## AddWhiteList
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Provider import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Validate Body for AddWhiteList route
def ULAddWhiteListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Route to add a number to the whitelist of the user
class AddWhiteList(Resource):
    def post(self):
        body = fquest.get_json()
        if not ULAddWhiteListValidation(body):
            return BadRequestError("bad requst"), 400

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        guid = data['guid']
        number = body["number"]
        WhitelistDb.addWhitelistNumberForUser(guid, number)
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200
