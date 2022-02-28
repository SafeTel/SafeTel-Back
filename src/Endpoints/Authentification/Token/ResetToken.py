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
from Endpoints.Utils.Request import validateBody

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

from Models.Endpoints.Authentification.Token.ResetTokenResponse import ResetTokenResponse

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

        Response = ResetTokenResponse(jwtConv.Serialize(guid, role))

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return Response.ToDict(), 200
