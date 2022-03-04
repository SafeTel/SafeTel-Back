##
## EPITECH PROJECT, 2022
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
# High level usage DB
from Infrastructure.Factory.UserFactory.Lists.Blacklist import Blacklist
from Infrastructure.Factory.UserFactory.Lists.Whitelist import Whitelist

### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Lists.Greylist.GetGreylistRequest import GetGreylistRequest
from Models.Endpoints.Account.Lists.Greylist.GreylistResponse import GreylistResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


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
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def get(self):
        Request = GetGreylistRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        Response = GreylistResponse(
            User.Blacklist.PullList().PhoneNumbers,
            User.Whitelist.PullList().PhoneNumbers
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
