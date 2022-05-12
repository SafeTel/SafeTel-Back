##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Whitelist
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
from Infrastructure.Factory.UserFactory.Lists.Whitelist import Whitelist

### MODELS
# Model Request & Response import
from Models.Endpoints.Account.Lists.Shared.ListGetRequest import ListGetRequest
from Models.Endpoints.Account.Lists.Shared.NumberRequest import NumberRequest
from Models.Endpoints.Account.Lists.Whitelist.WhitelistResponse import WhitelistResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/account/lists/whitelist?token=
###
# Response:
# {
# 	"Whitelist": [
# 		"example"
# 	]
# }
###
# Request:
# POST: localhost:2407/account/lists/whitelist
# {
# 	"token": "",
# 	"number": "example"
# }
###
# Response:
# {
# 	"Whitelist": [
# 		"example"
# 	]
# }
###
# Request:
# DELETE: localhost:2407/account/lists/whitelist
# {
# 	"token": "",
# 	"number": "example"
# }
###
# Response:
# {
# 	"Whitelist": [
# 		"example"
# 	]
# }
###


# Route to interract with Whitelist
class Whitelist(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Account/Lists/Whitelist/Swagger-Whitelist-GET.yml")
    def get(self):
        Request = ListGetRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = WhitelistResponse(
            User.Whitelist.PullList().PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    @swag_from("../../../../swagger/Account/Lists/Whitelist/Swagger-Whitelist-GET.yml")
    def post(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = WhitelistResponse(
            User.Whitelist.AddNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    @swag_from("../../../../swagger/Account/Lists/Whitelist/Swagger-Whitelist-GET.yml")
    def delete(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = WhitelistResponse(
            User.Whitelist.DeleteNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
