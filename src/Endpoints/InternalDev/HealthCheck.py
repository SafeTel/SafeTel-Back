##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HealthCheck
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Client mongo db import
from flask.globals import request

# Utils imports
import json

# JWT imports
from Models.Logic.Shared.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError

# Health CHeck Service
from Infrastructure.Services.HealthCheck.HealthCheckService import HealthCheckService

class HealthCheck(Resource):
    def get(self):
        hcService = HealthCheckService()
        jwtConv = JWTConvert()

        token = request.args["token"]

        if request.args.get("token") == None:
            return BadRequestError("bad token"), 400

        serverDatas = hcService.RunInfraCheck()
        serverEnvDatas = hcService.RunSoftCheck()

        serverCheck = {}
        envCheck = {}

        for x in serverDatas:
            if type(x) == type(''):
                serverCheck = json.loads(x)
        for x in serverEnvDatas:
            if type(x) == type(''):
                envCheck = json.loads(x)

        deserializedJWT = jwtConv.Deserialize(token)

        if (deserializedJWT == None):
            return BadRequestError("bad token"), 400
        elif (deserializedJWT["role"] == Roles.ADMIN or deserializedJWT["role"] == Roles.DEVELOPER):
            return self.DevDTO(serverCheck, envCheck)

        return {
            "healthCheck": {
                "server": serverCheck,
                "environment": envCheck
            }
        }

    def DevDTO(self, serverCheck, envCheck):
        del serverCheck['results']

        del envCheck['process']['environ']
        del envCheck['process']['pid']

        return {
            "healthCheck": {
                "server": serverCheck,
                "environment": envCheck
            }
        }
