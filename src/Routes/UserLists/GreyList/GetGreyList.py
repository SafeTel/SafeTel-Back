##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetGreyList
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# JWT import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.BlackListDB import BlacklistDB
from DataBases.Melchior.WhiteListDB import WhitelistDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()

# Route to get the white & black list of the user
class GetGreyList(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad token"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"],
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
