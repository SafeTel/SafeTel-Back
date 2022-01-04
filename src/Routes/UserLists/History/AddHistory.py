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
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB import
from DataBases.Melchior.HistoryDB import HistoryDB

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

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        guid = data['guid']
        number = body["number"]
        origin = body["origin"]
        time = body["time"]
        HistoryDb.addHistoryCallForUser(guid, number, origin, int(time))
        return {
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200
