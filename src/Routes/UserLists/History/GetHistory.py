##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetHistory
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# DB import
from src.DataBases.Melchior import HistoryDB

HistoryDb = HistoryDB()

class GetHistory(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'History': HistoryDb.getHistoryForUser(userId)["history"]
        }, 200
