##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CheckToken
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# jwt provider import
from Routes.Utils.JWTProvider.Provider import IsValidJWT

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Route to check a JWT
class CheckToken(Resource):
    def get(self):
        jwt = request.args["token"]
        if jwt is None:
            return BadRequestError("bad request"), 400

        validity = IsValidJWT(jwt)
        if (validity == None):
            return BadRequestError("the token is not a JWT"), 400

        return {
            'validity': validity,
        }, 200
