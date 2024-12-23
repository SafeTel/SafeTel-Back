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
# Error Manager import
from Models.Endpoints.Errors.ErrorManager import ErrorManager
### MODELS
# Model Request & Response import
from Models.Endpoints.Account.Infos.GetInfosRequest import GetInfosRequest
from Models.Endpoints.Account.Infos.GetInfosResponse import GetInfosResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


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
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    @swag_from("../../../../swagger/Account/Infos/Swagger-GetInfos.yml")
    def get(self):
        Request = GetInfosRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        UserInfos = User.PullUserInfos()
        Response = GetInfosResponse(
            UserInfos.email,
            UserInfos.username,
            UserInfos.CustomerInfos,
            UserInfos.Localization
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
