##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Greylist
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# JWT import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

# Models Request & Response imports
from Models.Endpoints.Account.Lists.GreylistResponse import GreylistResponse

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()

# Route to get the white & black list of the user
class GreyList(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad token"), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        guid = JwtInfos.guid

        response = GreylistResponse(
            BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"],
            WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        )

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
