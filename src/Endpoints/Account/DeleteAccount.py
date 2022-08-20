##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DeleteAccount
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory

### MODELS
# Model Request & Response import
from Models.Endpoints.Account.DeleteAccountRequest import DeleteAccountRequest
from Models.Endpoints.Account.DeleteAccountResponse import DeleteAccountResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# DELETE: localhost:2407/account/delete
# {
# 	"token": "",
# 	"username": "Megumin"
# }
###
# Response:
# {
# 	"deleted": true
# }
###


# Route to delete an account from an auth user
class DeleteAccount(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    @swag_from("../../../../swagger/Account/Swagger-DeleteAccount.yml")
    def delete(self):
        Request = DeleteAccountRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        if (User.PullUserInfos().username == Request.username):
            User.Delete()

        Response = DeleteAccountResponse(User.IsDeleted())

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
