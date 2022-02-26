##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetHistory
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

# Utils import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

HistoryDb = HistoryDB()

# Route to get the whitelist of the user
class GetHistory(Resource):
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
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200