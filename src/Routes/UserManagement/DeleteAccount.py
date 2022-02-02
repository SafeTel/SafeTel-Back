##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DeleteAccount
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Utils.MelchiorUtils import deleteDocumentForUser, isDeletedDocumentForUser

UserDb = UserDB()

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

        jwtDeserialized = DeserializeJWT(body["token"], Roles.USER)
        if jwtDeserialized is None:
            return BadRequestError('bad token'), 400

        guidUsr = jwtDeserialized['guid']

        result = UserDb.getUserByGUID(guidUsr)
        if result is None:
            return BadRequestError("bad token"), 400

        if result["userName"] != body["userName"]:
            return BadRequestError("manual security check failed"), 400

        deleteDocumentForUser(guidUsr)

        if isDeletedDocumentForUser(guidUsr):
            UserDb.deleteUser(guidUsr)

        return {
            'deleted': UserDb.exists(result['email'])
        }, 200
