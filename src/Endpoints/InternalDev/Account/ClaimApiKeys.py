##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ApiKeys
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

# DB imports
from Infrastructure.Services.MongoDB.Casper.Contributors import ContributorsDB
from Infrastructure.Services.MongoDB.Casper.ApiKeys import ApiKeyLogDB

# secret import
import secrets

from Models.Endpoints.InternalDev.Account.ClaimAPIKeyRequest import ClaimAPIKeyRequest
from Models.Endpoints.InternalDev.Account.ClaimAPIKeyResponse import ClaimAPIKeyResponse

ContributorsDb = ContributorsDB()
ApiKeyLogDb = ApiKeyLogDB()

# Route to know if an update is required for the embeded software
class ClaimApiKeys(Resource):
    def post(self):
        EndptErrorManager = EndpointErrorManager()
        Request = ClaimAPIKeyRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        claimer = Request.name

        if (not ContributorsDb.IsContributor(claimer)):
            return EndptErrorManager.CreateBadRequestError("You are not a contributor"), 400

        if (ApiKeyLogDb.isApiKeyForContributor(claimer, request.remote_addr)):
            return EndptErrorManager.CreateBadRequestError("You already own an apiKey"), 400

        apiKey = secrets.token_urlsafe(32)
        ApiKeyLogDb.logClaimeApiKey(apiKey, claimer, request.remote_addr)

        Response = ClaimAPIKeyResponse(apiKey)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
