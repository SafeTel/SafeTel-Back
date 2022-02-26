##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DelHistory
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
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

HistoryDb = HistoryDB()

# Validate Body for DelHistory route
def ULDelHistoryValidation(data):
    if not validateBody(
        data,
        ["token", "number", "time"]):
        return False
    return True

# Route to del a call from the history
class DelHistory(Resource):
    def delete(self):
        body = fquest.get_json()
        if not ULDelHistoryValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        time = body["time"]
        HistoryDb.delHistoryCallForUser(guid, number, time)
        return {
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200
