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
from Models.Endpoints.Embedded.LoginBox.LoginBoxRequest import LoginBoxRequest
from Models.Endpoints.Embedded.LoginBox.LoginBoxResponse import LoginBoxResponse

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
        self.__BoxDB = BoxDB()


    @swag_from("../../../../swagger/Embedded/")
    def post(self):
        Request = LoginBoxRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        guid = self.__BoxDB.RSUserByBoxID(Request.boxid)
        if (guid == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        User = self.__UserFactory.LoadUser(guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = LoginBoxResponse(
            self.__JwtConv.Serialize(
                guid,
                User.PullUserInfos().role
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
