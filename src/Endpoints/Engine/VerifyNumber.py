##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## VerifyNumber
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
from Models.Endpoints.Engine.VerifyNumberRequest import VerifyNumberRequest
from Models.Endpoints.Engine.VerifyNumberResponse import VerifyNumberResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvertEmbedded import JWTConvertEmbedded
# Engine
from Engine.Logic.Engine import Engine


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/engine/verify-number
# {
# 	"token": "456789",
# 	"number": "0123456789"
# }
###
# Response:
# {
# 	"block": true
# }
###


# Route to evaluate a number from an auth user
class VerifyNumber(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()
        self.__Engine = Engine()


    # TODO: ROUTE CHANGE: Fix postman tests
    @swag_from("../../../../swagger/Engine/Swagger-VerifyNumber.yml")
    def post(self):
        Request = VerifyNumberRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        if (not User.Box.IsClaimedByUser(JwtInfos.boxid)):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        if (not User.Box.IsBoxInCall(JwtInfos.boxid)):
            User.Box.UpdateCall(JwtInfos.boxid, True)
        else:
            return self.__ErrorManagerFactory.BadRequestError({"details": "This box is already in a call"}).ToDict(), 403

        verificationResult = self.__Engine.Verify(
            User,
            JwtInfos.boxid,
            Request.number
        )

        if (type(verificationResult) is str):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        Response = VerifyNumberResponse(
            verificationResult
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
