##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Login
##

### LOGIC
# Request Error
from urllib.request import Request
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError
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

from Models.Endpoints.Authentification.LoginRequest import LoginRequest
from Models.Endpoints.Authentification.LoginResponse import LoginResponse

# Route to log in a user
class Login(Resource):
    def post(self):
        Request = LoginRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        user = UserDb.getUser(Request.email)
        if user == None:
            return BadRequestError("this email is not linked to an account"), 400

        pwdConv = PWDConvert()
        if not pwdConv.Compare(Request.password, user["password"]):
            return BadRequestError('you can not connect with this combination of email and password'), 400

        jwtConv = JWTConvert()
        role = jwtConv.SToRoles(user["role"])
        guid = user["guid"]

        Response = LoginResponse(user["userName"], jwtConv.Serialize(guid, role))

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return Response.ToDict(), 200
