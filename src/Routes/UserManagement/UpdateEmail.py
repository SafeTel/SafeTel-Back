##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## UpdateEmail
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# validate Body for Update email route
def UMUpdateEmailBodyValidation(data):
    if not validateBody(
        data,
        ["token", "email"]):
        return False
    return True
"""     if not isValidEmail(data["email"]):
        return False """

# Route to update the email of an account from an auth user
class UpdateEmail(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMUpdateEmailBodyValidation(body):
            return BadRequestError('bad request'), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        result = UserDb.getUserByGUID(deserializedJWT['guid'])
        if result is None:
            return BadRequestError("bad token"), 400

        UserDb.UpdateAccountEmail(deserializedJWT['guid'], body['email'])

        return {
            'updated': not UserDb.exists(result['email'])
        }, 200

