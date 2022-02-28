##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Whitelist
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Models Request & Response imports
from Models.Endpoints.Account.Lists.NumberRequest import NumberRequest
from Models.Endpoints.Account.Lists.NumberResponse import NumberResponse

# Route to add a number to the whitelist of the user
class Whitelist(Resource):
    def get(self):
        token = fquest.args["token"]
        if token is None:
            return BadRequestError("Bad Request"), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        guid = JwtInfos.guid

        response = NumberResponse(WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        Request = NumberRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        WhitelistDb.addWhitelistNumberForUser(JwtInfos.guid, Request.number)

        response = NumberResponse(WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def delete(self):
        Request = NumberRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        WhitelistDb.delWhitelistNumberForUser(JwtInfos.guid, Request.number)

        response = NumberResponse(WhitelistDb.getWhitelistForUser(JwtInfos.guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
