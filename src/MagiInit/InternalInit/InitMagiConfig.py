##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitMagiConfig
##

### LOGIC
import os
import json

### INFRA
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class InitMagiConfig():
    def __init__(self):
        self.__IsValidConfig()
        self.__CheckEnvVars()
        self.__Ping()
        self.__SecurityLaunchCheck()


    def __IsValidConfig(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement Denied")
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            configMode = config["Mode"]
            if ("launchMode" not in configMode
            or "message" not in configMode
            or "launchSecurity" not in configMode
            or "MandatoryEnvVars" not in config):
                raise ValueError("FATAL ERROR: Configuration Denied")


    def __CheckEnvVars(self):
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("FATAL ERROR: Environement Denied")


    def __Ping(self):
        httpClient = HttpClient()
        pingUri = os.getenv("PING_URI")
        if httpClient.Ping(pingUri) is None:
            raise ValueError("FATAL ERROR: Environement Denied")


    def __SecurityLaunchCheck(self):
        with open("config.json", 'r') as JsonFile:
            config = json.load(JsonFile)
            launchMode = config["Mode"]["launchMode"]
            launchSecurity = config["Mode"]["launchSecurity"]
            if (launchSecurity):
                if (launchMode != "DEV"
                and launchMode != "PROD"
                and launchMode != "POSTMAN"):
                    raise ValueError("FATAL ERROR: Launch Mode Denied")
