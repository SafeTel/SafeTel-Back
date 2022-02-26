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

# JWT import
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

# Route to check a JWT
class CheckToken(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        validity = jwtConv.IsValid(token)
        if validity is None:
            return BadRequestError("bad token"), 400

        return {
            'validity': validity
        }, 200
