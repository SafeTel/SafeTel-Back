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
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB

# Models Request & Response imports
from Models.Endpoints.Account.Lists.GetGreyListRequest import GetGreylistRequest
from Models.Endpoints.Account.Lists.GreylistResponse import GreylistResponse

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()

# Route to get the white & black list of the user
class GreyList(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        Request = GetGreylistRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        guid = JwtInfos.guid

        response = GreylistResponse(
            BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"],
            WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"]
        )

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200
