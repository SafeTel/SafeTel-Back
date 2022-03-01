##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GetInfos
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Models Response imports
from Models.Endpoints.Account.Infos.GetInfosResponse import GetInfosResponse
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### LOGC
# jwt provider import
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


# Route to get the information of a user
class GetInfos(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    def get(self):
        token = request.args["token"]
        if (token is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Request"), 400

        JwtInfos = self.__JwtConv.Deserialize(token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400
        if (JwtInfos.role != Roles.USER):
            return self.__EndpointErrorManager.CreateBadRequestError("This account is not a user account"), 400

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
