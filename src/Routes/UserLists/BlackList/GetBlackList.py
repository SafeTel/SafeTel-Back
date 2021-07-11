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

# DB import
from src.DataBases.Melchior import BlacklistDB

BlacklistDb = BlacklistDB()

class GetBlackList(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(userId)["phoneNumbers"]
        }, 200
