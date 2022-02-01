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
from Routes.Utils.JWTProvider.Roles import Roles
from Routes.Utils.JWTProvider.Provider import DeserializeJWT

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
            return BadRequestError("bad request"), 400, 400

        data = DeserializeJWT(body["token"], Roles.USER)
        if data is None:
            return BadRequestError("bad token"), 400

        result = UserDb.getUserByGUID(data['guid'])
        if result is None:
            return BadRequestError("bad token"), 400

        customerInfos = body["customerInfos"]
        localization = body["localization"]

        UpdatePersonalInfos(UserDb.Users, data['guid'], customerInfos, localization)

        return {
            'changed': True
        }, 200
