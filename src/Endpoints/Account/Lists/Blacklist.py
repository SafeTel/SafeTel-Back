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
# Error Manager Factory import
from Models.Endpoints.Errors.ErrorManager import ErrorManager


### MODELS
# Model Request & Response import
from Models.Endpoints.Account.Lists.Shared.ListGetRequest import ListGetRequest
from Models.Endpoints.Account.Lists.Shared.NumberRequest import NumberRequest
from Models.Endpoints.Account.Lists.Blacklist.BlacklistResponse import BlacklistResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


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
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Account/Lists/Blacklist/Swagger-Blacklist-GET.yml")
    def get(self):
        Request = ListGetRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = BlacklistResponse(
            User.Blacklist.PullList().PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200


    @swag_from("../../../../swagger/Account/Lists/Blacklist/Swagger-Blacklist-POST.yml")
    def post(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = BlacklistResponse(
            User.Blacklist.AddNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200


    @swag_from("../../../../swagger/Account/Lists/Blacklist/Swagger-Blacklist-DELETE.yml")
    def delete(self):
        Request = NumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = BlacklistResponse(
            User.Blacklist.DeleteNumber(Request.number).PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
