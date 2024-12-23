##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdatePassword
##

### INFRA
# Flask imports
import imp
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager import
from Models.Endpoints.Errors.ErrorManager import ErrorManager### MODELS
# Model Request & Response import
from Models.Endpoints.Authentification.LostPassword.UpdateLostPasswordRequest import UpdateLostPasswordRequest
from Models.Endpoints.Authentification.LostPassword.UpdateLostPasswordResponse import UpdateLostPasswordResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/auth/lost-password/update-password
# {
#     "token": ""
#     "password": "newpassword"
# }
###
# Response:
# {
#     "passwordupdated": true
# }
###


# Route to edit a lost password
class UpdateLostPassword(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Authentification/LostPassword/Swagger-UpdateLostPassword.yml")
    def patch(self):
        Request = UpdateLostPasswordRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None or not JwtInfos.lostpassord):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        UserInfos = User.PullUserInfos()

        if (not UserInfos.Administrative.passwordlost):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        User.UpdatePassword(Request.password)
        User.LostPasswordMode(False)

        Response = UpdateLostPasswordResponse(True)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200

