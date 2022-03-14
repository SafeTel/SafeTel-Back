##
## EPITECH PROJECT, 2022
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

### MODELS
# Model Request & Response import
from Models.Endpoints.Authentification.LoginRequest import LoginRequest
from Models.Endpoints.Authentification.LoginResponse import LoginResponse


###
# Request:
# POST: localhost:2407/auth/reset-password
# {
#     "email": "asukat@the.best"
# }
###
# Response:
# {
#     "status": "mail sent"
# }
###


# Route to auth a user
class ResetPassword(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__UserFactory = UserFactory()


    def post(self):
        Request = LoginRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400


        LoginStatus, result = self.__UserFactory.LoginUser(
            Request.email,
            Request.password
        )
        if (not LoginStatus):
            self.__EndpointErrorManager.CreateBadRequestError(result), 400

        guid = result
        User = self.__UserFactory.LoadUser(guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = LoginResponse(
            User.PullUserInfos().username,
            self.__JwtConv.Serialize(guid, User.PullUserInfos().role)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
