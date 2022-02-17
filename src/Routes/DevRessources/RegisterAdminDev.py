##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## RegisterAdminDev
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# utils imports
import uuid
import time

# Utils check imports
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.UserListsUtils import UserListsUtils

# DB imports
from DataBases.Casper.ApiKeys import ApiKeyLogDB

UserDb = UserDB()

ApiKeyLogDb = ApiKeyLogDB()

def DRRegisterAdminDevValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "apiKey", "role", "registration"]):
        return False
    if not validateBody(
        data["registration"],
        ["userName", "email", "password"]):
        return False
    if data["magicNumber"] != 84:
        return False
    return True

class RegisterAdminDev(Resource):
    def post(self):
        body = fquest.get_json()

        if not DRRegisterAdminDevValidation(body):
            return BadRequestError("bad request"), 400

        if (not ApiKeyLogDb.isValidApiKey(body['apiKey'])):
            return BadRequestError("apiKey is not valid"), 400

        registration = body['registration']

        if UserDb.exists(registration["email"]):
            return BadRequestError("this email is already linked to an account"), 400

        create_ts = time.time()
        guid = str(uuid.uuid4())

        registration['guid'] = guid
        registration['ts'] = create_ts

        if (not Roles.has_value(body['role'])):
            return BadRequestError("bad request"), 400
        role = Roles.USER

        if (body['role'] == 'admin'):
            role = Roles.ADMIN
        elif (body['role'] == 'dev'):
            role = Roles.DEVELOPER
        else:
            return BadRequestError("bad request"), 400

        UserDb.addUser(registration, role)

        ULUtils = UserListsUtils()
        ULUtils.CreateUserLists(guid)

        jwtConv = JWTConvert()
        return {
            'created': True,
            'userName': registration['userName'],
            'token': jwtConv.Serialize(guid, role)
        }
