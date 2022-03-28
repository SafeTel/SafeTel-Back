##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HealthCheckService
##

### INFRA
# Client mongo db import
import pymongo

### LOGIC
# Health Check imports
from healthcheck import HealthCheck as HealthCheckFromPackage
from healthcheck import EnvironmentDump
# Get env var import
import os

class HealthCheckService():
    def __init__(self):
        self.Infra = HealthCheckFromPackage()
        self.Infra.add_check(self.__IsReachableMongoDB)
        self.Infra.add_check(self.__IsReachableUserDB)
        self.Infra.add_check(self.__IsReachableBlackListDB)
        self.Infra.add_check(self.__IsReachableWhiteListDB)
        self.Infra.add_check(self.__IsReachableHistoryDB)

        self.Soft = EnvironmentDump()
        self.Soft.add_section("application", self.__GetSoftInfos)


    def RunInfraCheck(self):
        return self.Infra.run()


    def RunSoftCheck(self):
        return self.Soft.run()


    def __IsReachableMongoDB(self):
        try:
            uri = os.getenv("DB_URI")
            client = pymongo.MongoClient(uri)
            self.SafeTelDB = client.Melchior
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, "Safetel mongoDB available"


    def __IsReachableUserDB(self):
        try:
            _ = self.SafeTelDB.User
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, 'User collection available'


    def __IsReachableBlackListDB(self):
        try:
            _ = self.SafeTelDB.Blacklist
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, 'Blacklist collection available'


    def __IsReachableWhiteListDB(self):
        try:
            _ = self.SafeTelDB.Whitelist
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, 'Whitelist collection available'


    def __IsReachableHistoryDB(self):
        try:
            _ = self.SafeTelDB.History
        except Exception as e:
            return False,  "EXCEPTION FORMAT PRINT:\n{}".format(e)
        return True, 'History collection available'


    def __GetSoftInfos(self):
        return {
            "maintainer": "Safetel",
            "github_repo": "SafeTel-Back"
        }
