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
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

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
        EndptErrorManager = EndpointErrorManager()
        Request = DeleteAccountRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        guidUsr = JwtInfos.guid

        result = UserDb.getUserByGUID(guidUsr)
        if result is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        if (result["username"] != Request.username):
            return EndptErrorManager.CreateBadRequestError("manual security check failed"), 400

        Usr = User(guidUsr)
        Usr.Delete()

        response = DeleteAccountResponse(Usr.IsDeleted())

        responseErrors = response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return response.ToDict(), 200
