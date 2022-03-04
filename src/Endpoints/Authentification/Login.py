##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Login
##

### LOGIC
# Request Error
from urllib.request import Request
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# JWT import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Password encription import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert

### INFRA
# Network imports
from flask import request as fquest
from flask_restful import Resource
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# Model for Role import
from Models.Logic.Shared.Roles import Roles

from Models.Endpoints.Authentification.LoginRequest import LoginRequest
from Models.Endpoints.Authentification.LoginResponse import LoginResponse

# Route to log in a user
class Login(Resource):
    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = LoginRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        user = UserDb.getUser(Request.email)
        if user == None:
            return EndptErrorManager.CreateBadRequestError("this email is not linked to an account"), 400

        pwdConv = PWDConvert()
        if not pwdConv.Compare(Request.password, user["password"]):
            return EndptErrorManager.CreateBadRequestError('you can not connect with this combination of email and password'), 400

        jwtConv = JWTConvert()
        guid = user["guid"]

        Response = LoginResponse(user["username"], jwtConv.Serialize(guid, Roles.USER))

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
