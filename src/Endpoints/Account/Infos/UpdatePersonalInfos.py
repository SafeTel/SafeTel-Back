##
## EPITECH PROJECT, 2022
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
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdatePersonalInfosRequest import UpdatePErsonalInfosRequest
from Models.Endpoints.Account.Infos.UpdatePersonalInfosResponse import UpdatePersonalInfosResponse

### LOGIC
# Utils check imports
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# PATCH: localhost:2407/account/infos/update-infos
# {
#     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJndWlkIjoiZGM5YmFlNWMtM2RiZC00YzJkLWE4N2ItYjMzMDk3ZWFmY2RlIiwicm9sZSI6MywiZXhwIjoxNjQ2NDQ1Mjg3fQ.1uJVP20ev_sre1jwAroRRiZtV-ecbdbR_JJJ7oyLK7c",
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


# Route to Register a user
class UpdatePersonalInfos(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def patch(self):
        Request = UpdatePErsonalInfosRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        UserInfos = User.PullUserInfos()
        if (UserInfos.CustomerInfos.Deserialize() == Request.CustomerInfos.Deserialize()
        and UserInfos.Localization.Deserialize() == Request.Localization.Deserialize()):
            return self.__EndpointErrorManager.CreateBadRequestError("The given infos and current are the same"), 400

        User.UpdatePersonalInfos(Request.CustomerInfos, Request.Localization)

        Response = UpdatePersonalInfosResponse(
            UserInfos.CustomerInfos.Deserialize() == Request.CustomerInfos.Deserialize()
            and UserInfos.Localization.Deserialize() == Request.Localization.Deserialize()
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
