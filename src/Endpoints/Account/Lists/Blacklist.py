##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Blacklist
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Endpoints.Utils.Request import validateBody
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB

BlacklistDb = BlacklistDB()

from Models.Endpoints.Account.Lists.AddNumberRequest import AddNumberRequest
from Models.Endpoints.Account.Lists.AddNumberResponse import AddNumberResponse

# Validate Body for DelBlackList route
def ULDelBlackListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Validate Body for AddBlackList route
def ULAddBlackListValidation(data):
    if not validateBody(
        data,
        ["token", "number"]):
        return False
    return True

# Route to add a number to the blacklist of the user
class Blacklist(Resource):
    def get(self):
        token = fquest.args["token"]
        if token is None:
            return BadRequestError("bad token"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']

        response = AddNumberResponse(BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        body = fquest.get_json()
        if not ULAddBlackListValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        BlacklistDb.addBlacklistNumberForUser(guid, body["number"])
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200


    def delete(self):
        body = fquest.get_json()
        if not ULDelBlackListValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = body["number"]
        BlacklistDb.delBlacklistNumberForUser(guid, number)
        return {
            'BlackList': BlacklistDb.getBlacklistForUser(guid)["PhoneNumbers"]
        }, 200
