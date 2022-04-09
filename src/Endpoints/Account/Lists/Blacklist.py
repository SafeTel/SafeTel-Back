##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Blacklist
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# High level usage DB
from Infrastructure.Factory.UserFactory.Lists.Blacklist import Blacklist

### MODELS
# Model Request & Response import
from Models.Endpoints.Account.Lists.Shared.ListGetRequest import ListGetRequest
from Models.Endpoints.Account.Lists.Shared.NumberRequest import NumberRequest
from Models.Endpoints.Account.Lists.Blacklist.BlacklistResponse import BlacklistResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# GET: localhost:2407/account/lists/blacklist?token=
###
# Response:
# {
# 	"Blacklist": [
# 		"example"
# 	]
# }
###
# Request:
# POST: localhost:2407/account/lists/blacklist
# {
# 	"token": "",
# 	"number": "example"
# }
###
# Response:
# {
# 	"Blacklist": [
# 		"example"
# 	]
# }
###
# Request:
# DELETE: localhost:2407/account/lists/blacklist
# {
# 	"token": "",
# 	"number": "example"
# }
###
# Response:
# {
# 	"Blacklist": [
# 		"example"
# 	]
# }
###


# Route to interract with Blacklist
class Blacklist(Resource):
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

        Response = BlacklistResponse(
            User.Blacklist.PullList().PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    def post(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = BlacklistResponse(
            User.Blacklist.AddNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    def delete(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = BlacklistResponse(
            User.Blacklist.DeleteNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
