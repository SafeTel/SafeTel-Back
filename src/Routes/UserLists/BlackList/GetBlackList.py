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
from DataBases.Melchior.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

class GetBlackList(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(userId)["PhoneNumbers"]
        }, 200
