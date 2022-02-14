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
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Route go get the whitelist of the user
class GetWhiteList(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200
