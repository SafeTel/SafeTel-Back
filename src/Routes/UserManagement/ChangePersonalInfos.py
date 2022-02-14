##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ChnagePersonalInfos
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
from datetime import datetime, timedelta
import uuid
import time

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidNumber
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Melchior.InternalUtils.DataWorker import UpdatePersonalInfos

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

        UpdatePersonalInfos(UserDb.Users, deserializedJWT['guid'], customerInfos, localization)

        return {
            'changed': True
        }, 200
