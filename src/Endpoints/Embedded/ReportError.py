##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ReportError
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
from Models.Endpoints.Embedded.ReportError.ReportErrorRequest import ReportErrorRequest
from Models.Endpoints.Embedded.ReportError.ReportErrorResponse import ReportErrorResponse

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
#     "token": "YTFUGYIHIJ",
#     "error": {
#        "trace": "File test.py, line 26, in <module> \n File urequests.py, line 108, in get \n File urequests.py, line 53, in request",
#		 "ts": 123456789,
#        "message":  "-202",
#        "type":  "OSError"
#     }
# }
###
# Response:
# {
# 	  "received": true
# }
###


# Route to Report an error from the embedded
class ReportError(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Embedded/Swagger-ReportError.yml")
    def post(self):
        Request = ReportErrorRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError(), 403

        if (not User.Box.IsClaimedByUser(JwtInfos.boxid)):
            return self.__ErrorManager.ForbiddenAccessError(), 403

        if (not User.Box.IsRegisteredBoxIp(JwtInfos.boxid, request.remote_addr)):
            return self.__ErrorManager.ProxyAuthenticationRequiredError(), 407

        User.Box.AddErrorReport(JwtInfos.boxid, Request.Error)

        Response = ReportErrorResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError(), 500
        return Response.ToDict(), 200
