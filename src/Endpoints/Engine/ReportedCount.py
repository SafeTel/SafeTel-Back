##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ReportedCount
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
from Models.Endpoints.Engine.ReportedCountRequest import ReportedCountRequest
from Models.Endpoints.Engine.ReportedCountResponse import ReportedCountResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Engine
from Engine.Logic.Engine import Engine

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/engine/reported-count?token=
###
# Response:
# {
#	"count": 42
# }
###


# Route to get the number of reported numbers
class ReportedCount(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()
        self.__Engine = Engine()


    @swag_from("../../../../swagger/Engine/Swagger-ReportedCount.yml")
    def get(self):
        Request = ReportedCountRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        count = self.__Engine.ReportedCount()
        Response = ReportedCountResponse(
            count
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
