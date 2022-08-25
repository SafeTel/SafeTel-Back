##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## CheckToken
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
from Models.Endpoints.Authentification.Token.CheckTokenRequest import CheckTokenRequest
from Models.Endpoints.Authentification.Token.CheckTokenResponse import CheckTokenResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/auth/check-token?token=
###
# Response:
# {
# 	"validity": true
# }
###


# Route to check a JWT
class CheckToken(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Authentification/Token/Swagger-CheckToken.yml")
    def get(self):
        Request = CheckTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        if (self.__UserFactory.LoadUser(JwtInfos.guid) == None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = CheckTokenResponse(
            self.__JwtConv.IsValid(Request.token)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
