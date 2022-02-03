##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GetInfos
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# jwt provider import
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB

UserDb = UserDB()

# Route to get the information from a user
class GetInfos(Resource):
    def get(self):
        jwt = request.args["token"]
        if jwt is None:
            return BadRequestError("bad request"), 400

        data = DeserializeJWT(jwt, Roles.USER)
        guid = data["guid"]

        if (data == None):
            return BadRequestError("this account is not a user account"), 400

        user = UserDb.getUserByGUID(guid)

        return {
            "email": user["email"],
            "userName": user["userName"],
            "customerInfos": {
                "firstName": user["customerInfos"]["firstName"],
                "lastName": user["customerInfos"]["lastName"],
                "phoneNumber": user["customerInfos"]["phoneNumber"]
            },
            "localization": {
                "country": user["localization"]["country"],
                "region": user["localization"]["region"],
                "adress": user["localization"]["adress"]
            }
        }, 200

    def UserInfosDTO(user):
        del user["_id"]
        del user["password"]
        del user['role']
        del user['time']
        del user['guid']
        return user
