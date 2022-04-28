##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Register
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
from Models.Endpoints.Authentification.RegisterRequest import RegisterRequest
from Models.Endpoints.Authentification.RegisterResponse import RegisterResponse
# Model for Role import
from Models.Logic.Shared.Roles import Roles

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Password encription import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/auth/register
# {
#     "magicnumber": 42,
#     "email": "asuka@the.cutest",
#     "username": "Megumin",
#     "password": "pwd",
#     "CustomerInfos": {
#         "firstName": "Megumin",
#         "lastName": "Konosuba",
#         "phoneNumber": "0100000000"
#     },
#     "Localization": {
#         "country": "Terra",
#         "region": "4568",
#         "address": "2 view Useless Aqua"
#     }
# }
###
# Response:
# {
# 	"created": true,
# 	"username": "Megumin",
# 	"token": ""
# }
###


# Route to Register a user
class Register(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Authentification/Swagger-Register.yml")
    def post(self):
        Request = RegisterRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        if (self.__UserFactory.IsMailRegitered(Request.email)):
            return self.__EndpointErrorManager.CreateBadRequestError("This email is already linked to an account"), 400

        User = self.__UserFactory.CreateUser(Request)
        UserInfos = User.PullUserInfos()

        Response = RegisterResponse(
            self.__UserFactory.IsUser(UserInfos.guid),
            UserInfos.username,
            self.__JwtConv.Serialize(User.GetGUID(), Roles.USER)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
