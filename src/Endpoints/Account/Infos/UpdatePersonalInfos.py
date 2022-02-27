##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ChnagePersonalInfos
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Endpoints.Utils.Types import isValidNumber
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

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
        body = fquest.get_json()
        request = UpdatePErsonalInfosRequest(body)

        requestErrors = request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        result = UserDb.getUserByGUID(deserializedJWT['guid'])
        if result is None:
            return BadRequestError("bad token"), 400

        customerInfos = request.CustomerInfos.ToDict()
        localization = request.Localization.ToDict()

        UserDb.UpdatePersonalInfos(deserializedJWT['guid'], customerInfos, localization)

        response = UpdatePersonalInfosResponse(True)

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
