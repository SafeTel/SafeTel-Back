##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Login
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager import
from Models.Endpoints.Errors.ErrorManager import ErrorManager### MODELS
# Model Request & Response import
from Models.Endpoints.Authentification.LoginRequest import LoginRequest
from Models.Endpoints.Authentification.LoginResponse import LoginResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/auth/login
# {
#     "magicnumber": 42,
#     "email": "asukat@the.best",
#     "password": "pwd"
# }
###
# Response:
# {
# 	"username": "Megumin",
# 	"token": ""
# }
###


# Route to auth a user
class Login(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Authentification/Swagger-Login.yml")
    def post(self):
        Request = LoginRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        LoginStatus, result = self.__UserFactory.LoginUser(
            Request.email,
            Request.password
        )
        if (not LoginStatus):
            self.__ErrorManager.BadRequestError(result).ToDict(), 400

        guid = result
        User = self.__UserFactory.LoadUser(guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = LoginResponse(
            User.PullUserInfos().username,
            self.__JwtConv.Serialize(guid, User.PullUserInfos().role)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
