##
## EPITECH PROJECT, 2022
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
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
from Endpoints.Utils.Request import validateBody

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
# DB imports
from Infrastructure.Services.MongoDB.Casper.ApiKeys import ApiKeyLogDB
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

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

        if (not Roles.HasValue(body['role'])):
            return BadRequestError("bad request"), 400
        role = Roles.USER

        if (body['role'] == 'admin'):
            role = Roles.ADMIN
        elif (body['role'] == 'dev'):
            role = Roles.DEVELOPER
        else:
            return BadRequestError("bad request"), 400

        UserDb.addUser(registration, role)

        self.BlacklistDb = BlacklistDB()
        self.WhitelistDb = WhitelistDB()
        self.HistoryDb = HistoryDB()
        self.BlacklistDb.newBlacklist(guid)
        self.WhitelistDb.newWhitelist(guid)
        self.HistoryDb.newHistory(guid)

        jwtConv = JWTConvert()
        return {
            'created': True,
            'userName': registration['userName'],
            'token': jwtConv.Serialize(guid, role)
        }
