##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EvaluateCall
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
from Models.Endpoints.Engine.EvaluateCallRequest import EvaluateCallRequest
from Models.Endpoints.Engine.EvaluateCallResponse import EvaluateCallResponse

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
# 	"report": true,
#   "Call": {
#       "number": "01345678",
#       "status": "Received",
#       "time": 3456789
#   }
# }
###
# Response:
# {
# 	"message": OK
# }
###


# Route to evaluate a number from an auth user
class EvaluateCall(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()
        self.__Engine = Engine()


    # TODO: ROUTE CHANGE: Fix postman tests
    @swag_from("../../../../swagger/Engine/Swagger-EvaluateCall.yml")
    def post(self):
        Request = EvaluateCallRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        if (not User.Box.IsClaimedByUser(JwtInfos.boxid)):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        if (not User.Box.IsRegisteredBoxIp(JwtInfos.boxid, request.remote_addr)):
            return self.__ErrorManager.ProxyAuthenticationRequiredError(), 407

        if (User.Box.IsBoxInCall(JwtInfos.boxid)):
            User.Box.UpdateCall(JwtInfos.boxid, False)
        else:
            return self.__ErrorManager.BadRequestError("A report must be sent at the end of a call").ToDict(), 403

        self.__Engine.ProcessCall(
            User,
            JwtInfos.boxid,
            Request.report,
            Request.Call
        )

        Response = EvaluateCallResponse(
            "OK"
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
