##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CheckToken
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# jwt provider import
from Routes.Utils.JWTProvider.Provider import IsValidJWT

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Validate Body for CheckToken route
def UMCheckTokenBodyValidation(data):
    if not validateBody(
        data,
        ["token"]):
        return False
    return True

# Route to check a JWT
class CheckToken(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMCheckTokenBodyValidation(body):
            return BadRequestError("bad request"), 400

        validity = IsValidJWT(body["token"])
        if (validity == None):
            return BadRequestError("the token is not a JWT"), 400

        return {
            'validity': validity,
        }, 200
