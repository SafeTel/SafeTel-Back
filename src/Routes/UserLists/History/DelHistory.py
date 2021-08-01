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

# DB import
from DataBases.Melchior import HistoryDB

HistoryDb = HistoryDB()

class DelHistory(Resource):
    def delete(self):
        if not validateBody(fquest.get_json(), ["userId", "number", "time"]):
            return {
                'error': 'bad_request'
            }, 400
        body = fquest.get_json()
        userId = body["userId"]
        number = body["number"]
        time = body["time"]
        HistoryDb.delHistoryCallForUser(userId, number, time)
        return {
            'History': HistoryDb.getHistoryForUser(userId)["history"]
        }, 200
