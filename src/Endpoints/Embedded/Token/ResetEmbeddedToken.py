##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ResetEmbeddedToken
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
from Models.Endpoints.Embedded.Token.ResetEmbeddedToken.ResetEmbeddedTokenRequest import ResetEmbeddedTokenRequest
from Models.Endpoints.Embedded.Token.ResetEmbeddedToken.ResetEmbeddedTokenResponse import ResetEmbeddedTokenResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvertEmbedded import JWTConvertEmbedded


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/embedded/token/reset-embedded?token=
###
# Response:
# {
# 	"token": "new token"
# }
###


# Route to reset a JWT
class ResetEmbeddedToken(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Embedded/Token/Swagger-ResetEmbeddedToken.yml")
    def get(self):
        Request = ResetEmbeddedTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        if (not User.Box.IsRegisteredBoxIp(JwtInfos.boxid, request.remote_addr)):
            return self.__EndpointErrorManager.CreateProxyAuthenticationRequired(), 407

        Response = ResetEmbeddedTokenResponse(
            self.__JwtConv.Serialize(
                JwtInfos.guid,
                JwtInfos.boxid
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
