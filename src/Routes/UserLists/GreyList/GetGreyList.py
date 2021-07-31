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
from DataBases.Melchior.BlackListDB import BlacklistDB
from DataBases.Melchior.WhiteListDB import WhitelistDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()

class GetGreyList(Resource):
    def get(self):
        userId = request.args["userId"]
        return {
            'WhiteList': WhitelistDb.getWhitelistForUser(userId)["PhoneNumbers"],
            'BlackList': BlacklistDb.getBlacklistForUser(userId)["PhoneNumbers"]
        }, 200
