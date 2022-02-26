##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## AddHistory
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Endpoints.Utils.Request import validateBody
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

HistoryDb = HistoryDB()

# Validate Body for DelHistory route
def ULAddHistoryValidation(data):
    if not validateBody(
        data,
        ["token", "number", "origin", "time"]):
        return False
    return True

# Route to del a call from the history
class AddHistory(Resource):
    def post(self):
        body = fquest.get_json()
        if not ULAddHistoryValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        origin = body["origin"]
        time = body["time"]
        HistoryDb.addHistoryCallForUser(guid, number, origin, int(time))
        return {
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200
