##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ReverseReport
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
from Models.Endpoints.Embedded.ReverseEvaluation.ReverseEvaluationRequest import ReverseEvaluationRequest
from Models.Endpoints.Embedded.ReverseEvaluation.ReverseEvaluationResponse import ReverseEvaluationResponse

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
# POST: localhost:2407/embedded/reverse-evaluation
# {
#     "token": "putain je me suis pris une pause de 30 min aujourdhui pour me dire que ma doc est pas assez precise",
#     "number": "lel"
# }
###
# Response:
# {
# 	  "updated": true
# }
###


# Route to Block Unblock a Number
class ReverseEvaluation(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvertEmbedded(os.getenv("JWT_EMBEDDED_DURATION"))
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Embedded/Swagger-ReverseEvaluation.yml")
    def post(self):
        Request = ReverseEvaluationRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        if (not User.Box.IsClaimedByUser(JwtInfos.boxid)):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        if (User.Blacklist.IsNumber(Request.number)):
            User.Blacklist.DeleteNumber(Request.number)
        else:
            User.Blacklist.AddNumber(Request.number)

        Response = ReverseEvaluationResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
