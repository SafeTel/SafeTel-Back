##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CheckToken
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
from Models.Endpoints.Authentification.Token.CheckTokenRequest import CheckTokenRequest
from Models.Endpoints.Authentification.Token.CheckTokenResponse import CheckTokenResponse
# Model for Role import
from Models.Logic.Shared.Roles import Roles

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# GET: localhost:2407/auth/check-token?token=
###
# Response:
# {
# 	"validity": true
# }
###


# Route to check a JWT
class CheckToken(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def get(self):
        Request = CheckTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        if (self.__UserFactory.LoadUser(JwtInfos.guid) == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = CheckTokenResponse(
            self.__JwtConv.IsValid(Request.token)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
