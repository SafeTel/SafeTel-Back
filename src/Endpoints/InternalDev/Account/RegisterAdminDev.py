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

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
# DB imports
from Infrastructure.Services.MongoDB.Casper.ApiKeys import ApiKeyLogDB
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

from Models.Endpoints.InternalDev.Account.RegisterAdminDevRequest import RegisterAdminDevRequest
from Models.Endpoints.InternalDev.Account.RegisterAdminDevResponse import RegisterAdminDevResponse

UserDb = UserDB()

ApiKeyLogDb = ApiKeyLogDB()

class RegisterAdminDev(Resource):
    def post(self):
        Request = RegisterAdminDevRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        if (not ApiKeyLogDb.isValidApiKey(Request.apiKey)):
            return BadRequestError("apiKey is not valid"), 400

        Registrattion = Request.Registrattion

        if UserDb.exists(Registrattion.email):
            return BadRequestError("this email is already linked to an account"), 400

        create_ts = time.time()
        guid = str(uuid.uuid4())

        registrate = Registrattion.ToDict()
        registrate['guid'] = guid
        registrate['ts'] = create_ts

        if (not Roles.HasValue(Request.role)):
            return BadRequestError("bad request"), 400
        role = Roles.USER

        if (Request.role == 'admin'):
            role = Roles.ADMIN
        elif (Request.role == 'dev'):
            role = Roles.DEVELOPER
        else:
            return BadRequestError("bad request"), 400

        UserDb.addUser(registrate, role)

        self.BlacklistDb = BlacklistDB()
        self.WhitelistDb = WhitelistDB()
        self.HistoryDb = HistoryDB()
        self.BlacklistDb.newBlacklist(guid)
        self.WhitelistDb.newWhitelist(guid)
        self.HistoryDb.newHistory(guid)

        jwtConv = JWTConvert()

        Response = RegisterAdminDevResponse(
            True,
            registrate['userName'],
            jwtConv.Serialize(guid, role)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return Response.ToDict(), 200
