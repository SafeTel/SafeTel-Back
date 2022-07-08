##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ApiKeys
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory# DB imports (doesn't need High Level interface since it's internal dev)
from Infrastructure.Services.MongoDB.Casper.Contributors import ContributorsDB
from Infrastructure.Services.MongoDB.Casper.ApiKeys import ApiKeyLogDB

### MODELS
# Model Request & Response import
from Models.Endpoints.InternalDev.Account.ClaimAPIKeyRequest import ClaimAPIKeyRequest
from Models.Endpoints.InternalDev.Account.ClaimAPIKeyResponse import ClaimAPIKeyResponse

### LOGC
# API key encryption import
import secrets


###
# Request:
# POST: localhost:2407/account/infos/update-email
# {
# 	"magicnumber": 42,
# 	"name": ""
# }
###
# Response:
# {
# 	"apiKey": "",
# 	"message": "only one apikey is allowed for an contributor or ip"
# }
###


# Route to get an API key
class ClaimApiKeys(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.ContributorsDb = ContributorsDB()
        self.ApiKeyLogDb = ApiKeyLogDB()


    def post(self):
        Request = ClaimAPIKeyRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        claimer = Request.name

        if (not self.ContributorsDb.IsContributor(claimer)):
            return self.__ErrorManagerFactory.BadRequestError({"details": "You are not a contributor"}).ToDict(), 400

        if (self.ApiKeyLogDb.isApiKeyForContributor(claimer, request.remote_addr)):
            return self.__ErrorManagerFactory.BadRequestError({"details": "You already have an apiKey"}).ToDict(), 400

        apiKey = secrets.token_urlsafe(32)
        self.ApiKeyLogDb.logClaimeApiKey(apiKey, claimer, request.remote_addr)

        Response = ClaimAPIKeyResponse(apiKey)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
