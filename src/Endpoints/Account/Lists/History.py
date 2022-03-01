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
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# DB import
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

from Models.Endpoints.Account.Lists.HistoryResponse import HistoryResponse
from Models.Endpoints.Account.Lists.AddHistoryRequest import AddHistoryRequest
from Models.Endpoints.Account.Lists.DelHistoryRequest import DelHistoryRequest

HistoryDb = HistoryDB()

class History(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        token = fquest.args["token"]
        if token is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        guid = JwtInfos.guid

        response = HistoryResponse(HistoryDb.getHistoryForUser(guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200


    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = AddHistoryRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        HistoryDb.addHistoryCallForUser(
            JwtInfos.guid,
            Request.number,
            Request.status,
            Request.time
        )

        response = HistoryResponse(HistoryDb.getHistoryForUser(JwtInfos.guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200

    def delete(self):
        EndptErrorManager = EndpointErrorManager()
        Request = AddHistoryRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        response = HistoryResponse(HistoryDb.getHistoryForUser(JwtInfos.guid)["History"])

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200