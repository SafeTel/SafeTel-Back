##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HealthCheck
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# Health CHeck Service
from Infrastructure.Services.HealthCheck.HealthCheckService import HealthCheckService

### MODELS
# Model Request & Response import
from Models.Endpoints.InternalDev.HealthCheckRequest import HealthCheckRequest
# Model for Role import
from Models.Logic.Shared.Roles import Roles

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# JSON  lib import
import json



class HealthCheck(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__HealthCheckService = HealthCheckService()


    def get(self):
        Request = HealthCheckRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        if (JwtInfos.role == Roles.USER):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        serverDatas = self.__HealthCheckService.RunInfraCheck()
        serverEnvDatas = self.__HealthCheckService.RunSoftCheck()

        serverCheck = {}
        envCheck = {}

        for x in serverDatas:
            if type(x) == type(''):
                serverCheck = json.loads(x)
        for x in serverEnvDatas:
            if type(x) == type(''):
                envCheck = json.loads(x)

        return {
            "healthCheck": {
                "server": serverCheck,
                "environment": envCheck
            }
        }, 200
