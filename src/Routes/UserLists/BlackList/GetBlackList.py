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
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

# Route to get the blacklist of the user
class GetBlackList(Resource):
    def get(self):
        data = DeserializeJWT(request.args["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        guid = data['guid']
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
