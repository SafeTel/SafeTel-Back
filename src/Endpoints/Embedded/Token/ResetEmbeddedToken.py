##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ResetEmbeddedToken
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
from Models.Endpoints.Embedded.Token.ResetEmbeddedToken.ResetEmbeddedTokenRequest import ResetEmbeddedTokenRequest
from Models.Endpoints.Embedded.Token.ResetEmbeddedToken.ResetEmbeddedTokenResponse import ResetEmbeddedTokenResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvertEmbedded import JWTConvertEmbedded
# OS environement var import
import os

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/embedded/token/reset-embedded?token=
###
# Response:
# {
# 	"token": "new token"
# }
###


# Route to reset a JWT
class ResetEmbeddedToken(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvertEmbedded(int(os.getenv("JWT_EMBEDDED_DURATION")))
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Embedded/Token/Swagger-ResetEmbeddedToken.yml")
    def get(self):
        Request = ResetEmbeddedTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        if (self.__UserFactory.LoadUser(JwtInfos.guid) == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = ResetEmbeddedTokenResponse(
            self.__JwtConv.Serialize(
                JwtInfos.guid,
                JwtInfos.boxid
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
