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
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']

        response = NumberResponse(WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        body = fquest.get_json()

        request = NumberRequest(body)

        requestErrors = request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        WhitelistDb.addWhitelistNumberForUser(guid, number)

        response = NumberResponse(WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def delete(self):
        body = fquest.get_json()

        request = NumberRequest(body)

        requestErrors = request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        WhitelistDb.delWhitelistNumberForUser(guid, number)

        response = NumberResponse(WhitelistDb.getWhitelistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
