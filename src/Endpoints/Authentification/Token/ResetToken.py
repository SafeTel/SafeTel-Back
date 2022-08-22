##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ResetToken
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory
### MODELS
# Model Request & Response import
from Models.Endpoints.Authentification.Token.ResetTokenRequest import ResetTokenRequest
from Models.Endpoints.Authentification.Token.ResetTokenResponse import ResetTokenResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/auth/reset-token?token=
###
# Response:
# {
# 	"token": ""
# }
###


# Route to reset a JWT
class ResetToken(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Authentification/Token/Swagger-ResetToken.yml")
    def get(self):
        Request = ResetTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError("Bad Token").ToDict(), 401

        if (self.__UserFactory.LoadUser(JwtInfos.guid) == None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        Response = ResetTokenResponse(
            self.__JwtConv.Serialize(
                JwtInfos.guid,
                JwtInfos.role
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
