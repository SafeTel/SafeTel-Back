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
from Endpoints.Utils.Request import validateBody
from Endpoints.Utils.Types import isValidNumber
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# validate Body for Register route
def UMChangesPersonalInfosValidation(data):
    if not validateBody(
        data,
        ["token", "customerInfos", "localization"]):
        return False
    if not validateBody(
        data["customerInfos"],
        ["firstName", "lastName", "phoneNumber"]):
        return False
    if not isValidNumber(data["customerInfos"]["phoneNumber"]):
        return False
    if not validateBody(
        data["localization"],
        ["country", "region", "adress"]):
        return False
    return True

# Route to Register a user
class ChangesPersonalInfos(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMChangesPersonalInfosValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        result = UserDb.getUserByGUID(deserializedJWT['guid'])
        if result is None:
            return BadRequestError("bad token"), 400

        customerInfos = body["customerInfos"]
        localization = body["localization"]

        UserDb.UpdatePersonalInfos(deserializedJWT['guid'], customerInfos, localization)

        return {
            'changed': True
        }, 200