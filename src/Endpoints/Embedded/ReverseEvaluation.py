##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ReverseReport
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager import
from Models.Endpoints.Errors.ErrorManager import ErrorManager
### MODELS
# Model Request & Response import
from Models.Endpoints.Embedded.ReverseEvaluation.ReverseEvaluationRequest import ReverseEvaluationRequest
from Models.Endpoints.Embedded.ReverseEvaluation.ReverseEvaluationResponse import ReverseEvaluationResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvertEmbedded import JWTConvertEmbedded


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/embedded/reverse-evaluation
# {
#     "token": "trdfytguyhiujoiko",
#     "number": "lel"
# }
###
# Response:
# {
# 	  "updated": true
# }
###


# Route to Block Unblock a Number
class ReverseEvaluation(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Embedded/Swagger-ReverseEvaluation.yml")
    def post(self):
        Request = ReverseEvaluationRequest(request.get_json())

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

        if (User.Blacklist.IsNumber(Request.number)):
            User.Blacklist.DeleteNumber(Request.number)
        else:
            User.Blacklist.AddNumber(Request.number)

        Response = ReverseEvaluationResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
