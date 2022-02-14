##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Login
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# JWT import
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Password encription import
from Routes.Utils.PWDSerialiazer.Serializer import CheckPWD

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB

UserDb = UserDB()

# validate Body for Login route
def UMLoginBodyValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "email", "password"]):
        return False
    if data["magicNumber"] != 42:
        return False
    return True

# Route to log in a user
class Login(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMLoginBodyValidation(body):
            return BadRequestError("bad request"), 400

        user = UserDb.getUser(body["email"])
        if user == None:
            return BadRequestError("this email is not linked to an account"), 400

        if not CheckPWD(body["password"], user["password"]):
            return BadRequestError('you can not connect with this combination of email and password'), 400

        jwtConv = JWTConvert()
        role = jwtConv.SToRoles(user["role"])
        guid = user["guid"]

        return {
            'userName': user["userName"],
            'token': jwtConv.Serialize(guid, role)
        }, 200
