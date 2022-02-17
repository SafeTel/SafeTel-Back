##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ResetToken
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# jwt provider import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()

# Route to reset a JWT
class ResetToken(Resource):
    def get(self):
        token = request.args["token"]
        if token is None:
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(token)
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guid = deserializedJWT["guid"]
        role = deserializedJWT["role"]

        if (UserDb.existByGUID(guid) == False):
            return BadRequestError("you are not registred")

        return {
            'token': jwtConv.Serialize(guid, role),
        }, 200
