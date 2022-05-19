##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateBoxMode
##

### INFRA
# Flask imports
import imp
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Model Request & Response import
from Models.Endpoints.Box.UpdateBoxMode.UpdateBoxModeRequest import UpdateBoxModeRequest
from Models.Endpoints.Box.UpdateBoxMode.UpdateBoxModeResponse import UpdateBoxModeResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# OS environement var import
import os

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/box/update-severity
# {
#     "token": "jwt",
#     "boxid": "1234567890",
#     "severity": "normal"
# }
###
# Response:
# {
#       "updated": true
# }
###


# Route to update a box severity
class UpdateSeverity(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert(os.getenv("JWT_FRONTEND_DURATION"))
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Box/Swagger-UpdateSeverity.yml")
    def patch(self):
        Request = UpdateBoxModeRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        error = User.Box.UpdateSeverity(
            Request.boxid,
            Request.severity
        )

        if (error != None):
            return self.__EndpointErrorManager.CreateForbiddenAccessErrorWithMessage(error), 403

        Response = UpdateBoxModeResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
