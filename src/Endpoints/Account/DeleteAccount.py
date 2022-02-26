##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DeleteAccount
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Routes.Utils.Request import validateBody
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()


from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
from Infrastructure.Factory.UserFactory.User import User

# Validate Body for DeleteAccount route
def UMDeleteAccountBodyValidation(data):
    if not validateBody(
        data,
        ["token", "userName"]):
        return False
    return True

# Route to delete an account from an auth user
class DeleteAccount(Resource):
    def delete(self):
        body = fquest.get_json()
        if not UMDeleteAccountBodyValidation(body):
            return BadRequestError("bad request"), 400

        jwtConv = JWTConvert()

        deserializedJWT = jwtConv.Deserialize(body["token"])
        if deserializedJWT is None:
            return BadRequestError("bad token"), 400

        guidUsr = deserializedJWT['guid']

        result = UserDb.getUserByGUID(guidUsr)
        if result is None:
            return BadRequestError("bad token"), 400

        if result["userName"] != body["userName"]:
            return BadRequestError("manual security check failed"), 400

        Usr = User(guidUsr)
        Usr.Delete()

        return {
            'deleted': Usr.IsDeleted()
        }, 200
