##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## ApiKeys
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# Utils check imports
from Routes.Utils.Request import validateBody

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# DB imports
from DataBases.Casper.Contributors import ContributorsDB
from DataBases.Casper.ApiKeys import ApiKeyLogDB

# secret import
import secrets

ContributorsDb = ContributorsDB()
ApiKeyLogDb = ApiKeyLogDB()

def DRClaimApiKeysValidation(data):
    if not validateBody(
        data,
        ["name", "magicNumber"]):
        return False
    if data["magicNumber"] != 84:
        return False
    return True

# Route to know if an update is required for the embeded software
class ClaimApiKeys(Resource):
    def post(self):
        body = fquest.get_json()

        if not DRClaimApiKeysValidation(body):
            return BadRequestError("bad request"), 400

        claimer = body["name"]

        if (not ContributorsDb.IsContributor(claimer)):
            return BadRequestError("you are not a contributor"), 400

        if (ApiKeyLogDb.isApiKeyForContributor(claimer, request.remote_addr)):
            return BadRequestError("you already own an apiKey"), 400

        apiKey = secrets.token_urlsafe(32)
        ApiKeyLogDb.logClaimeApiKey(apiKey, claimer, request.remote_addr)

        return {
            "apiKey": apiKey,
            "message": "only one apikey is allowed for an contributor or ip"
        }