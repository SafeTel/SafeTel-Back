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
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

# Models Response imports
from Models.Endpoints.Account.Infos.GetInfosResponse import GetInfosResponse
from Models.Endpoints.SharedJObject.AccountInfos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.AccountInfos.Localization import Localization

UserDb = UserDB()

# Route to get the information from a user
class GetInfos(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT["guid"]

        if (deserializedJWT["role"] != Roles.USER):
            return BadRequestError("this account is not a user account"), 400

        user = UserDb.getUserByGUID(guid)

        responseLocalization = Localization(user["localization"])
        responseCustomerInfos = CustomerInfos(user["customerInfos"])
        response = GetInfosResponse(user["email"], user["userName"], responseCustomerInfos, responseLocalization)

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200

    def UserInfosDTO(user):
        del user["_id"]
        del user["password"]
        del user['role']
        del user['time']
        del user['guid']
        return user
