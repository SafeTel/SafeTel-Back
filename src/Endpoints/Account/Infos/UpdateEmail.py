##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateEmail
##

### INFRA
# Flask imports
from flask import request as fquest
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory

### MODELS
# Models Request & Response imports
from Models.Endpoints.Account.Infos.UpdateEmailRequest import UpdateEmailRequest
from Models.Endpoints.Account.Infos.UpdateEmailResponse import UpdateEmailResponse

### LOGIC
# Utils check imports
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/account/infos/update-email
# {
# 	"token": "heyiloveevangelion",
# 	"email": "asuka@the.best"
# }
###
# Response:
# {
# 	"updated": false
# }
###


# Route to update the email of an account
class UpdateEmail(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()

    @swag_from("../../../../swagger/Account/Infos/Swagger-UpdateEmail.yml")
    def patch(self):
        Request = UpdateEmailRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        User.UpdateEmail(Request.email)

        Response = UpdateEmailResponse(
            User.PullUserInfos().email == Request.email
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
