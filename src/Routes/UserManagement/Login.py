##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Login
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
from datetime import datetime, timedelta

# jwt provider import
from Routes.Utils.JWTProvider.Roles import Roles
from Routes.Utils.JWTProvider.Provider import SerializeJWT, StrToRole

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
            return BadRequestError("this email is not linked to an account")

        if not CheckPWD(body["password"], user["password"]):
            return BadRequestError('you can not connect with this combination of email and password')

        role = StrToRole(user["role"])

        return {
            'userName': user["userName"],
            'token': SerializeJWT(user["guid"], role)
        }, 200
