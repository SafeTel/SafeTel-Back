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
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# File Logging
from Infrastructure.Utils.FileLogger.FileLogger import FileLogger

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
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()
        self.__FileLogger = FileLogger()

    @swag_from("../../../../swagger/Account/Infos/Swagger-UpdateEmail.yml")
    def patch(self):
        JsonRequest = fquest.get_json()

        self.__LoggingRequest(str(JsonRequest))
        Request = UpdateEmailRequest(JsonRequest)

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        User.UpdateEmail(Request.email)

        Response = UpdateEmailResponse(
            User.PullUserInfos().email == Request.email
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        ## TODO: Fix using an after_response middleware
        self.__LoggingResponse(Response.ToDict(), 200)
        return Response.ToDict(), 200

    def __LoggingRequest(self, request: str):
        self.__FileLogger.LoggingObjects("Update Email", "Request Json", request)

    def __LoggingResponse(self, request: dict, httpCode: int):
        self.__FileLogger.LoggingObjects("Update Email", "UpdateEmailResponse with status " + str(httpCode), str(request))