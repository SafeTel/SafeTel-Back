##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetWhiteList
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# DB import
from DataBases.Melchior import WhitelistDB

WhitelistDb = WhitelistDB()

class GetWhiteList(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(userId)["phoneNumbers"]
        }, 200
