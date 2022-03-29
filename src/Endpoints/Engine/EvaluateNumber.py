##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## EvaluateNumber
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
from Models.Endpoints.Engine.EvaluateNumberRequest import EvaluateNumberRequest
from Models.Endpoints.Engine.EvaluateNumberResponse import EvaluateNumberResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# DELETE: localhost:2407/engine/evaluate-number
# {
# 	"token": "",
# 	"number": "0123456789"
# }
###
# Response:
# {
# 	"block": true
# }
###


# Route to evaluate a number from an auth user
class EvaluateNumber(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    def delete(self):
        Request = EvaluateNumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = EvaluateNumberResponse(
            # TODO: see if the number should be blocked or not
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200

