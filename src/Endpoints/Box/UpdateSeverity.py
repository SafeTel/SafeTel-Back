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
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory
### MODELS
# Model Request & Response import
from Models.Endpoints.Box.UpdateBoxMode.UpdateBoxModeRequest import UpdateBoxModeRequest
from Models.Endpoints.Box.UpdateBoxMode.UpdateBoxModeResponse import UpdateBoxModeResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


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
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Box/Swagger-UpdateSeverity.yml")
    def patch(self):
        Request = UpdateBoxModeRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        error = User.Box.UpdateSeverity(
            Request.boxid,
            Request.severity
        )

        if (error != None):
            return self.__ErrorManagerFactory.ForbiddenAccessErrorWithMessage({"details": error}).ToDict(), 403

        Response = UpdateBoxModeResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
