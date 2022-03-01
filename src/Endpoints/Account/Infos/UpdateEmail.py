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
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdateEmailRequest import UpdateEmailRequest
from Models.Endpoints.Account.Infos.UpdateEmailResponse import UpdateEmailResponse

# Route to update the email of an account from an auth user
class UpdateEmail(Resource):
    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = UpdateEmailRequest(fquest.get_json())

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

        UserDb.UpdateAccountEmail(JwtInfos.guid, Request.email)

        response = UpdateEmailResponse(UserDb.exists(result['email']))

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
