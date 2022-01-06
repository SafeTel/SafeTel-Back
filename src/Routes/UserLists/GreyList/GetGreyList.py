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

# Utils import
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

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
        data = DeserializeJWT(request.args["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        guid = data['guid']
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"],
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
