##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DelHistory
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# DB import
from DataBases.Melchior.HistoryDB import HistoryDB

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
            return {
                'error': 'bad_request'
            }, 400

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        guid = data['guid']
        number = body["number"]
        time = body["time"]
        HistoryDb.delHistoryCallForUser(guid, number, time)
        return {
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200
