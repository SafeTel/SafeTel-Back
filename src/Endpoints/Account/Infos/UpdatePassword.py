##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdatePassword
##

### INFRA
# Flask imports
from flask import request as fquest
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory


### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdatePasswordrequest import UpdatePasswordRequest
from Models.Endpoints.Account.Infos.UpdatePasswordResponse import UpdatePasswordResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Password converter import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/account/infos/update-password
# {
#     "token": "",
#     "oldpassword": "pwd",
#     "newpassword": "newpwd",
# }
###
# Response:
# {
# 	  "updated": false
# }
###


# Route to update passwword of an account
class UpdatePassword(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()
        self.__PWDConvert = PWDConvert()


    @swag_from("../../../../swagger/Account/Infos/Swagger-UpdatePassword.yml")
    def patch(self):
        Request = UpdatePasswordRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        UserInfos = User.PullUserInfos()
        hashednewpassword = self.__PWDConvert.Serialize(Request.newpassword)
        if (UserInfos.password == hashednewpassword):
            return self.__ErrorManagerFactory.BadRequestError({"details": "The old and new password are the same"}).ToDict(), 400

        User.UpdatePassword(Request.newpassword)

        UserInfos = User.PullUserInfos()
        Response = UpdatePasswordResponse(
            UserInfos.password == hashednewpassword
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200

