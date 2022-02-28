##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DeleteAccount
##

# Network imports
from urllib import response
from urllib.request import Request
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Endpoints.Utils.Request import validateBody
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

UserDb = UserDB()


from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
from Infrastructure.Factory.UserFactory.User import User

# Models Request & Response imports
from Models.Endpoints.Account.DeleteAccountRequest import DeleteAccountRequest
from Models.Endpoints.Account.DeleteAccountResponse import DeleteAccountResponse

# Route to delete an account from an auth user
class DeleteAccount(Resource):
    def delete(self):
        Request = DeleteAccountRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return BadRequestError("bad token"), 400

        guidUsr = JwtInfos.guid

        result = UserDb.getUserByGUID(guidUsr)
        if result is None:
            return BadRequestError("bad token"), 400

        if result["username"] != Request.userName:
            return BadRequestError("manual security check failed"), 400

        Usr = User(guidUsr)
        Usr.Delete()

        response = DeleteAccountResponse(Usr.IsDeleted())

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return response.ToDict(), 200
