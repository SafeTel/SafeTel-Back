##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Greylist
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Lists.Greylist.GetGreylistRequest import GetGreylistRequest
from Models.Endpoints.Account.Lists.Greylist.GreylistResponse import GreylistResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# OS environement var import
import os

### SWAGGER
# flasgger import
from flasgger.utils import swag_from

###
# Request:
# GET: localhost:2407/account/lists/greylist?token=
###
# Response:
# {
# 	"Blacklist": [
# 		"example1"
# 	],
# 	"Whitelist": [
# 		"example2"
# 	],
# }
###


# Route to get the white & black list of the user
class GreyList(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert(os.getenv("JWT_FRONTEND_DURATION"))
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Account/Lists/Greylist/Swagger-Greylist.yml")
    def get(self):
        Request = GetGreylistRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = GreylistResponse(
            User.Blacklist.PullList().PhoneNumbers,
            User.Whitelist.PullList().PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
