##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## HealthCheck
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Client mongo db import
from flask.globals import request
import pymongo

# Import db name and db URI
from config import dbname, URI_MELCHIOR

# Health Check imports
from healthcheck import HealthCheck as HealthCheckFromPackage
from healthcheck import EnvironmentDump

# Utils imports
import json
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Route to health check
class HealthCheck(Resource):
    def get(self):
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

        devRequest = DeserializeJWT(token, Roles.DEVELOPER)
        adminRequest = DeserializeJWT(token, Roles.ADMIN)

        if (devRequest == None and adminRequest == None):
            return BadRequestError("bad token"), 400
        elif (devRequest != None):
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
        client = pymongo.MongoClient(URI_MELCHIOR)
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
