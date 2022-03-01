##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ChnagePersonalInfos
##

# Network imports
from urllib.request import Request
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdatePersonalInfosRequest import UpdatePErsonalInfosRequest
from Models.Endpoints.Account.Infos.UpdatePersonalInfosResponse import UpdatePersonalInfosResponse

# Route to Register a user
class UpdatePersonalInfos(Resource):
    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = UpdatePErsonalInfosRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        result = UserDb.getUserByGUID(JwtInfos.guid)
        if result is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        UserDb.UpdatePersonalInfos(JwtInfos.guid, Request.CustomerInfos, Request.Localization)

        response = UpdatePersonalInfosResponse(True)

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200
