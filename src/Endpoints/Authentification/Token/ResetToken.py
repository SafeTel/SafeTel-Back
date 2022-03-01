##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ResetToken
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# jwt provider import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

from Models.Endpoints.Authentification.Token.ResetTokenRequest import ResetTokenRequest
from Models.Endpoints.Authentification.Token.ResetTokenResponse import ResetTokenResponse

UserDb = UserDB()

# Route to reset a JWT
class ResetToken(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        Request = ResetTokenRequest(request.args.to_dict())

        requestErrors = Request.ResetTokenRequest()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        JwtConv = JWTConvert()

        JwtInfos = JwtConv.Deserialize(Request.token)
        if JwtInfos is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        if (UserDb.existByGUID(JwtInfos.guid) == False):
            return EndptErrorManager.CreateBadRequestError("you are not registred")

        Response = ResetTokenResponse(
            JwtConv.Serialize(
                JwtInfos.guid,
                JwtInfos.role
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
