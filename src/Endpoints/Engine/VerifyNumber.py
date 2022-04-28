##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## VerifyNumber
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
from Models.Endpoints.Engine.VerifyNumberRequest import VerifyNumberRequest
from Models.Endpoints.Engine.VerifyNumberResponse import VerifyNumberResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/engine/verify-number
# {
# 	"token": "456789",
#   "boxid": "34567890",
# 	"number": "0123456789"
# }
###
# Response:
# {
# 	"block": true
# }
###


# Route to evaluate a number from an auth user
class VerifyNumber(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    # TODO: ROUTE CHANGE: Fix postman tests, Fixed in models, doc & swagger
    @swag_from("../../../../swagger/Engine/Swagger-VerifyNumber.yml")
    def post(self):
        Request = VerifyNumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = VerifyNumberResponse(
            User.Blacklist.IsNumber(Request.number)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
