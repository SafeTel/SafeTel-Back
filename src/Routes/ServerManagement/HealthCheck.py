##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## HealthCheck
##

# Network imports
import imp
from flask import request as fquest
from flask_restful import Resource

# Client mongo db import
from flask.globals import request
import pymongo

# Health Check imports
from healthcheck import HealthCheck as HealthCheckFromPackage
from healthcheck import EnvironmentDump

# Utils imports
import json

# JWT imports
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

import os

# Route to health check
class HealthCheck(Resource):
    def get(self):
        jwtConv = JWTConvert()

        token = request.args["token"]

        if request.args.get("token") == None:
            return BadRequestError("bad token"), 400

        self.serverCheck()
        serverDatas = self.health.run()
        serverEnvDatas = self.envdump.run()

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

    def serverCheck(self):
        self.health = HealthCheckFromPackage()
        self.envdump = EnvironmentDump()

        self.health.add_check(self.checkMongoDBAvailability)
        self.health.add_check(self.checkMongoDBCollectionAvailability_User)
        self.health.add_check(self.checkMongoDBCollectionAvailability_Blacklist)
        self.health.add_check(self.checkMongoDBCollectionAvailability_Whitelist)
        self.health.add_check(self.checkMongoDBCollectionAvailability_History)
        self.envdump.add_section("application", self.getSoftwareData)

    def checkMongoDBAvailability(self):
        client = pymongo.MongoClient(os.getenv("DB_URI"))
        # Check if we can access safetel database
        self.safetelDatabase = client.Melchior
        return True, "Safetel mongoDB available"

    # Check if we can access the collections
    def checkMongoDBCollectionAvailability_User(self):
        _ = self.safetelDatabase.User
        return True, 'User collection available'

    def checkMongoDBCollectionAvailability_Blacklist(self):
        _ = self.safetelDatabase.Blacklist
        return True, 'Blacklist collection available'

    def checkMongoDBCollectionAvailability_Whitelist(self):
        _ = self.safetelDatabase.Whitelist
        return True, 'Whitelist collection available'

    def checkMongoDBCollectionAvailability_History(self):
        _ = self.safetelDatabase.History
        return True, 'History collection available'

    def getSoftwareData(self):
        return {"maintainer": "Safetel",
            "github_repo": "SafeTel-Back"}
