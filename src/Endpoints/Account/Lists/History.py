##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## History
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Model Request & Response import
from Models.Endpoints.Account.Lists.Shared.ListGetRequest import ListGetRequest
from Models.Endpoints.Account.Lists.History.HistoryResponse import HistoryResponse
from Models.Endpoints.Account.Lists.History.AddHistoryRequest import AddHistoryRequest
from Models.Endpoints.Account.Lists.History.DelHistoryRequest import DelHistoryRequest

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# GET: localhost:2407/account/lists/history?token=
###
# Response:
# {
# 	"History": [
# 		{
# 			"number": "example",
# 			"status": "Blocked",
# 			"time": 1000
# 		}
# 	]
# }
###
# Request:
# POST: localhost:2407/account/lists/history
# {
# 	"token": "",
# 	"HistoryCall": {
# 		"number": "example",
# 		"status": "Blocked",
# 		"time": 1000
# 	}
# }
###
# Response:
# {
# 	"History": [
# 		{
# 			"number": "example",
# 			"status": "Blocked",
# 			"time": 1000
# 		}
# 	]
# }
###
# Request:
# DELETE: localhost:2407/account/lists/history
# {
# 	"token": "",
# 	"number": "example",
# 	"time": 1000
# }
###
# Response:
# {
# 	"History": [
# 		{
# 			"number": "example",
# 			"status": "Blocked",
# 			"time": 1000
# 		}
# 	]
# }
###


# Routes to interract with History
class History(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def get(self):
        Request = ListGetRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = HistoryResponse(
            User.History.PullList().History
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    def post(self):
        Request = AddHistoryRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        User.History.AddHistoryCall(Request.HistoryCall)

        response = HistoryResponse(
            User.History.PullList().History
        )

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200


    def delete(self):
        Request = DelHistoryRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        User.History.DeleteHistoryCall(
            Request.number,
            Request.time
        )

        Response = HistoryResponse(
            User.History.PullList().History
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
