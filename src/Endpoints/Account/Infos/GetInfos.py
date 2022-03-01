##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GetInfos
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# jwt provider import
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

# Models Response imports
from Models.Endpoints.Account.Infos.GetInfosResponse import GetInfosResponse
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

UserDb = UserDB()

# Route to get the information from a user
class GetInfos(Resource):
    def __init__(self):
        self.a = "a"

    def get(self):
        EndptErrorManager = EndpointErrorManager()
        token = request.args["token"]
        if token is None:
            return EndptErrorManager.CreateBadRequestError("Bad Request"), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(token)
        if (JwtInfos is None):
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        guid = JwtInfos.guid

        if (JwtInfos.role != Roles.USER):
            return EndptErrorManager.CreateBadRequestError("this account is not a user account"), 400

        user = UserDb.getUserByGUID(guid)

        responseLocalization = Localization(user["localization"])
        responseCustomerInfos = CustomerInfos(user["customerInfos"])
        response = GetInfosResponse(user["email"], user["username"], responseCustomerInfos, responseLocalization)

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200

    def UserInfosDTO(user):
        del user["_id"]
        del user["password"]
        del user['role']
        del user['time']
        del user['guid']
        return user
