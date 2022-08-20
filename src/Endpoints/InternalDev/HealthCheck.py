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
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory# Health CHeck Service
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


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# GET: localhost:2407/internaldev/healthCheck?token=
###
# Response:
# {
# 	"healthCheck": {
# 		"server": {
# 		},
# 		"environment": {
# 		}
# 	}
# }
###


# Route check the health of the server
class HealthCheck(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvert()
        self.__HealthCheckService = HealthCheckService()


    @swag_from("../../../../swagger/InternalDev/Swagger-HealthCheck.yml")
    def get(self):
        Request = HealthCheckRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError({"details": requestErrors}).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManagerFactory.BadRequestError({"details": "Bad Token"}).ToDict(), 401

        if (JwtInfos.role is Roles.USER):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

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
