##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ResetToken
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# jwt provider import
from Routes.Utils.JWTProvider.Provider import IsValidJWT, DeserializeBlindJWT, SerializeJWT

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB

UserDb = UserDB()

# Validate Body for ResetToken route
def UMResetTokenBodyValidation(data):
    if not validateBody(
        data,
        ["token"]):
        return False
    return True

# Route to reset a JWT
class ResetToken(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMResetTokenBodyValidation(body):
            return BadRequestError("bad request"), 400

        validity = IsValidJWT(body["token"])
        if (validity == None or validity == False):
            return BadRequestError("not a valid JWT"), 400

        jwtDeserialized = DeserializeBlindJWT(body["token"])
        guid = jwtDeserialized["guid"]
        role = jwtDeserialized["role"]

        if (UserDb.existByGUID(guid) == False):
            return BadRequestError("you are not registred")

        return {
            'token': SerializeJWT(guid, role),
        }, 200
