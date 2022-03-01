##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CheckToken
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# JWT import
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

from Models.Endpoints.Authentification.Token.CheckTokenRequest import CheckTokenRequest
from Models.Endpoints.Authentification.Token.CheckTokenResponse import CheckTokenResponse


# Route to check a JWT
class CheckToken(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        Request = CheckTokenRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        jwtConv = JWTConvert()

        validity = jwtConv.IsValid(Request.token)
        if validity is None:
            return EndptErrorManager.CreateBadRequestError("Bad Token"), 400

        Response = CheckTokenResponse(validity)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
