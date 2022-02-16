##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## config
##

###
import os
import json
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class InitiateServerConfig():
    def __init__(self):
        self.__CheckEnvVars()
        self.__Ping()


    def __CheckEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("Not a valid environement, missing mandatory env variable: " + mandatoryEnvVar)
        self.__Ping()


    def __Ping(self):
        httpClient = HttpClient()
        pingUri = os.getenv("PING_URI")
        if httpClient.IsUp(pingUri) == None:
            raise ValueError("Cannot ping " + pingUri + ", fatal error.")
