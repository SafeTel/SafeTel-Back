##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetInfos
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
# Model Request & Response import
from Models.Endpoints.Account.Infos.GetInfosRequest import GetInfosRequest
from Models.Endpoints.Account.Infos.GetInfosResponse import GetInfosResponse
# Model for Role import
from Models.Logic.Shared.Roles import Roles

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# GET: localhost:2407/account/infos/getInfos?token=
###
# Response:
# {
#	"email": "asukathebest@bbbb.cccc",
#	"username": "Megumin",
#	"CustomerInfos": {
#		"firstName": "Megumin",
#		"lastName": "Konosuba",
#		"phoneNumber": "0100000000"
#	},
#	"Localization": {
#		"country": "Terra",
#		"region": "4568",
#		"address": "2 view Useless Aqua"
#	}
# }
###


# Route to get the informations of an account
class GetInfos(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def get(self):
        Request = GetInfosRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        UserInfos = User.PullUserInfos()
        Response = GetInfosResponse(
            UserInfos.email,
            UserInfos.username,
            UserInfos.CustomerInfos,
            UserInfos.Localization
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
