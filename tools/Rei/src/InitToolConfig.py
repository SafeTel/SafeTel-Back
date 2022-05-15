##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## tool config
##

### LOGIC
import logging
# For Getenv
import os
# Load json
import json

### INFRA
# To perform Ping
import requests

class InitToolConfig():
    def __init__(self):
        self.__IsValidConfig()
        self.__CheckEnvVars()
        self.__Ping()

    def __IsValidConfig(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            if ("MandatoryEnvVars" not in config):
                raise ValueError("FATAL ERROR: Configuration Denied")

    def __CheckEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("FATAL ERROR: Environement Denied")

    def __Ping(self):
        pingUri = os.getenv("PING_URI")
        response = requests.get(pingUri)

        if (self.__IsValidResponse(response)):
            raise ValueError("FATAL ERROR: Environement Denied")

    def __IsValidResponse(self, response: requests.Response):
        NominalCode = 200
        NominalHeaders = [
            "text/json; charset=utf-8",
            "text/html; charset=UTF-8"
        ]

        if (response.status_code != NominalCode):
            return False
        for NominalHeader in NominalHeaders:
            if (response.headers == NominalHeader):
                return True
        return False
