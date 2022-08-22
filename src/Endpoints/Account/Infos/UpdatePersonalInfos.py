##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ChnagePersonalInfos
##

### INFRA
# Flask imports
from flask import request as fquest
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory
### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdatePersonalInfosRequest import UpdatePErsonalInfosRequest
from Models.Endpoints.Account.Infos.UpdatePersonalInfosResponse import UpdatePersonalInfosResponse

### LOGIC
# Utils check imports
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/account/infos/update-infos
# {
#     "token": "heygimmeajwt",
#     "CustomerInfos": {
#         "firstName": "Asuka",
#         "lastName": "be trong",
#         "phoneNumber": "$RVphoneNumber"
#     },
#     "Localization": {
#         "country": "$RVcountry",
#         "region": "$RVregion",
#         "address": "$RVadress"
#     }
# }
###
# Response:
# {
# 	"updated": false
# }
###


# Route to update personal infos of an account
class UpdatePersonalInfos(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    @swag_from("../../../../swagger/Account/Infos/Swagger-UpdatePersonalInfos.yml")
    def patch(self):
        ## TODO: PE -> Pe
        Request = UpdatePErsonalInfosRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return self.__ErrorManagerFactory.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        UserInfos = User.PullUserInfos()
        if (UserInfos.CustomerInfos.Deserialize() == Request.CustomerInfos.Deserialize()
        and UserInfos.Localization.Deserialize() == Request.Localization.Deserialize()):
            return self.__ErrorManagerFactory.BadRequestError("The given infos and current are the same").ToDict(), 400

        User.UpdatePersonalInfos(Request.CustomerInfos, Request.Localization)

        Response = UpdatePersonalInfosResponse(
            UserInfos.CustomerInfos.Deserialize() == Request.CustomerInfos.Deserialize()
            and UserInfos.Localization.Deserialize() == Request.Localization.Deserialize()
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
