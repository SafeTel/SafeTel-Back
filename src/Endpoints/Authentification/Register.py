##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Register
##

### LOGIC
# Utils check imports
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# Password encription import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert

### INFRA
# Network imports
from flask import request as fquest
from flask_restful import Resource
import uuid
import time
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
from Infrastructure.Factory.UserFactory.User import User

from Models.Endpoints.Authentification.RegisterRequest import RegisterRequest
from Models.Endpoints.Authentification.RegisterResponse import RegisterResponse

UserDb = UserDB()

# Route to Register a user
class Register(Resource):
    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = RegisterRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        if (UserDb.exists(Request.email)):
            return EndptErrorManager.CreateBadRequestError("this email is already linked to an account"), 400

        UsrFactory = UserFactory()
        body = fquest.get_json()
        User = UsrFactory.CreateUser(body)
        UserInfos = User.PullUserInfos()

        jwtConv = JWTConvert()
        Response = RegisterResponse(
            True,
            UserInfos.username,
            jwtConv.Serialize(User.GetGUID(), Roles.USER)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
