##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## HealthCheck
##

# Client mongo db import
from flask.globals import request
import pymongo

# Network imports
from flask import request as fquest
from flask_restful import Resource
from healthcheck import HealthCheck as HealthCheckFromPackage
from healthcheck import EnvironmentDump
import json

# Utils check imports
from Routes.Utils.Request import validateBody

# Melchior uri import
from DataBases.Melchior.MelchiorConfig import URI_MELCHIOR

# Route to health check
class HealthCheck(Resource):
    def get(self):
        if request.args["magicNumber"] != "42":
            return {
                'error': 'bad_request'
            }, 400

        self.serverCheck()

        serverDatas = self.health.run()
        serverEnvDatas = self.envdump.run()

        healthCheck = {}
        envCheck = {}

        for x in serverDatas:
            if type(x) == type(''):
                healthCheck = json.loads(x)

        for x in serverEnvDatas:
            if type(x) == type(''):
                envCheck = json.loads(x)

        return {
            "healthCheck": {
                "server": healthCheck,
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
