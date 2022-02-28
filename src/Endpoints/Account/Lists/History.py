##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## History
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

from Models.Endpoints.Account.Lists.HistoryResponse import HistoryResponse
from Models.Endpoints.Account.Lists.AddHistoryRequest import AddHistoryRequest
from Models.Endpoints.Account.Lists.DelHistoryRequest import DelHistoryRequest

HistoryDb = HistoryDB()

class History(Resource):
    def get(self):
        token = fquest.args["token"]
        if token is None:
            return BadRequestError("bad token"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']

        response = HistoryResponse(HistoryDb.getHistoryForUser(guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        request = AddHistoryRequest(fquest.get_json())

        requestErrors = request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(request.token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = request.number
        origin = request.status
        time = request.time
        HistoryDb.addHistoryCallForUser(guid, number, origin, int(time))

        response = HistoryResponse(HistoryDb.getHistoryForUser(guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200

    def delete(self):
        request = AddHistoryRequest(fquest.get_json())

        requestErrors = request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(request.token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT['guid']
        number = request.number
        time = request.time

        response = HistoryResponse(HistoryDb.getHistoryForUser(guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200