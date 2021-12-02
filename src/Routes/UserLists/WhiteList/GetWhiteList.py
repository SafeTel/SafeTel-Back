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
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Route go get the whitelist of the user
class GetWhiteList(Resource):
    def get(self):
        data = DeserializeJWT(request.args["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad request"), 400

        guid = data['guid']
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        }, 200
