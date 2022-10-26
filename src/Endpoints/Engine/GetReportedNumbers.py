##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetReportedNumbers
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
from Models.Endpoints.Engine.GetReportedNumbersRequest import GetReportedNumbersRequest
from Models.Endpoints.Engine.GetReportedNumbersResponse import GetReportedNumbersResponse

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
# GET: localhost:2407/engine/get-reported-numbers
# {
# 	"token": "456789",
# 	"index": 3
# }
###
# Response:
# {
#	"Numbers": [
#       "3812897321",
#       "7987897237",
#       "6676860986"
#   ]
# }
###


# Route to get the numbers by index
class GetReportedNumbers(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()
        self.__Engine = Engine()


    @swag_from("../../../../swagger/Engine/Swagger-GetReportedNumbers.yml")
    def post(self):
        Request = GetReportedNumbersRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = GetReportedNumbersResponse(
            self.__Engine.GetReportedNumbers(Request.index)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
