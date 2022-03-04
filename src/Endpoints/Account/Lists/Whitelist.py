##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Whitelist
##

# Network imports
from flask import request
from flask_restful import Resource

# Utils import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

WhitelistDb = WhitelistDB()

# Models Request & Response imports
from Models.Endpoints.Account.Lists.Shared.ListGetRequest import ListGetRequest
from Models.Endpoints.Account.Lists.Shared.NumberRequest import NumberRequest
from Models.Endpoints.Account.Lists.Whitelist.WhitelistResponse import WhitelistResponse

# Route to add a number to the whitelist of the user
class Whitelist(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        Request = ListGetRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        response = WhitelistResponse(WhitelistDb.getWhitelistForUser(JwtInfos.guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        WhitelistDb.addWhitelistNumberForUser(JwtInfos.guid, Request.number)

        response = WhitelistResponse(WhitelistDb.getWhitelistForUser(JwtInfos.guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200


    def delete(self):
        EndptErrorManager = EndpointErrorManager()
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        WhitelistDb.delWhitelistNumberForUser(JwtInfos.guid, Request.number)

        response = WhitelistResponse(WhitelistDb.getWhitelistForUser(JwtInfos.guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200
