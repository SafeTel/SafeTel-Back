##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## config
##

### LOGIC
import os
import json
from pathlib import Path

### INFRA
import requests

class AmaneConfig():
    def __init__(self, isForceLaunch = False):
        self.validationCode = 200
        self.__IsValidConfig()
        if isForceLaunch:
            self.__SecurityLaunchCheck()
        self.__SetEnvVars()
        self.__CheckEnvVars()
        self.__Ping()

    def __SecurityLaunchCheck(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            launchMode = config["Mode"]["launchMode"]
            launchSecurity = config["Mode"]["launchSecurity"]
            if (launchSecurity):
                if (launchMode != "DEV"
                and launchMode != "PROD"
                and launchMode != "POSTMAN"):
                    raise ValueError("FATAL ERROR: Launch Mode Denied")

    def __IsValidConfig(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            configMode = config["Mode"]
            if ("launchMode" not in configMode
            or "message" not in configMode
            or "launchSecurity" not in configMode
            or "MandatoryEnvVars" not in config):
                raise ValueError("FATAL ERROR: Configuration Denied")


    def __SetEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for envVarToSet in config["VariableToSetOptionally"]:
                os.environ[envVarToSet] = config["VariableToSetOptionally"][envVarToSet]


    def __CheckEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("FATAL ERROR: Environement Denied")


    def __Ping(self):
        pingUri = os.getenv("PING_URI")
        response = requests.get(pingUri)
        if (response.status_code != self.validationCode):
            raise ValueError("FATAL ERROR: Environement Denied")