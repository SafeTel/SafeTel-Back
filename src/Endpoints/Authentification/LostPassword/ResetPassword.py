##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ResetPassword
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# Service import
from Infrastructure.Services.GMail.GMail import GMail

### MODELS
# Model Request & Response import
from Models.Endpoints.Authentification.LostPassword.LostPasswordRequest import LostPasswordRequest
from Models.Endpoints.Authentification.LostPassword.LostPasswordResponse import LostPasswordResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
from Models.Infrastructure.Factory.UserFactory.UserInfos import UserInfos

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/auth/lost-password/reset-password
# {
#     "email": "asukat@the.best"
# }
###
# Response:
# {
#     "mailsent": true
# }
###


# Route to auth a user
class ResetPassword(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()
        self.__GMail = GMail()


    @swag_from("../../../../swagger/Authentification/LostPassword/Swagger-ResetPassword.yml")
    def post(self):
        Request = LostPasswordRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        User = self.__UserFactory.LoadUserByMail(Request.email)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        User.LostPasswordMode(True)
        UserInfos = User.PullUserInfos()

        token = self.__JwtConv.Serialize(
            UserInfos.guid,
            UserInfos.role,
            True
        )

        self.__GMail.SendMail(
            UserInfos.email,
            "SafeTel: " + UserInfos.username + " it looks like you lost your password",
            "safetel.fr/resetpassword?token=" + token
        )

        Response = LostPasswordResponse(True)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
