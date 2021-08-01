##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetGreyList
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# Utils import
from Routes.Utils.Request import validateBody

# DB import
from DataBases.Melchior import BlacklistDB, WhitelistDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()

class GetGreyList(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(userId)["phoneNumbers"],
            'BlackList': BlacklistDb.getBlacklistForUser(userId)["phoneNumbers"]
        }, 200
