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
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# import low level interface Box
from Infrastructure.Services.MongoDB.Balthasar.BoxDB import BoxDB

### MODELS
# Model Request & Response import
from Models.Endpoints.Embedded.ReverseReport.ReverseReportRequest import ReverseReportRequest
from Models.Endpoints.Embedded.ReverseReport.ReverseReportResponse import ReverseReportResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/embedded/reverse-report
# {
#     "token": "nan serieux allez voir SPY x FAMILY l'anime est juste parfait",
#     "boxid": "nan vraiment stop taffer, allez le voir",
#     "number": "au moins l'épisode 1 mdr"
# }
###
# Response:
# {
# 	  "updated": true
# }
###


# Route to Block Unblock a Number
class ReverseReport(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert(24)
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/embedded/")
    def post(self):
        Request = ReverseReportRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        if (not User.Box.IsClaimedByUser(Request.boxid)):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        if (User.Blacklist.IsNumber(Request.number)):
            User.Blacklist.DeleteNumber(Request.number)
        else:
            User.Blacklist.AddNumber(Request.number)

        Response = ReverseReportResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
