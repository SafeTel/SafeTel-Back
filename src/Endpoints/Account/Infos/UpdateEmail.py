##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateEmail
##

# Network imports
from urllib.request import Request
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Endpoints.Utils.Types import isValidEmail
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdateEmailRequest import UpdateEmailRequest
from Models.Endpoints.Account.Infos.UpdateEmailResponse import UpdateEmailResponse

# Route to update the email of an account from an auth user
class UpdateEmail(Resource):
    def post(self):
        Request = UpdateEmailRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        result = UserDb.getUserByGUID(JwtInfos.guid)
        if result is None:
            return BadRequestError("bad token"), 400

        UserDb.UpdateAccountEmail(JwtInfos.guid, Request.email)

        response = UpdateEmailResponse(UserDb.exists(result['email']))

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
