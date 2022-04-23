##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## config
##

### LOGIC
import logging
import os
import json
from pathlib import Path
from pickle import FALSE, TRUE

### INFRA
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class InitLocalServer():
    def __init__(self):
        isLocal = self.__LaunchCheck()
        if not isLocal:
            logging.warning("LaunchMode not Local. Cancelling Local Server Configuration")
        else:
            self.__CopyDataFromServer()

    def __LaunchCheck(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            launchMode = config["Mode"]["launchMode"]
            if (launchMode != "LOCAL"):
                return False
            return True

    def __CopyDataFromServer(self):
        logging.warning("Valid Copy")



    # def __IsValidConfig(self):
    #     if (not os.path.isfile("config.json")):
    #         raise ValueError("FATAL ERROR: Environement Denied")
    #     with open("config.json", 'r') as jsonFile:
    #         config = json.load(jsonFile)
    #         configMode = config["Mode"]
    #         if ("launchMode" not in configMode
    #         or "message" not in configMode
    #         or "launchSecurity" not in configMode
    #         or "MandatoryEnvVars" not in config):
    #             raise ValueError("FATAL ERROR: Configuration Denied")


    # def __CheckEnvVars(self):
    #     with open("config.json", 'r') as jsonFile:
    #         config = json.load(jsonFile)
    #         for mandatoryEnvVar in config["MandatoryEnvVars"]:
    #             if (mandatoryEnvVar in os.environ) == False:
    #                 raise ValueError("FATAL ERROR: Environement Denied")


    # def __Ping(self):
    #     httpClient = HttpClient()
    #     pingUri = os.getenv("PING_URI")
    #     if httpClient.Ping(pingUri) == None:
    #         raise ValueError("FATAL ERROR: Environement Denied")


    # def __SecurityLaunchCheck(self):
    #     with open("config.json", 'r') as jsonFile:
    #         config = json.load(jsonFile)
    #         launchMode = config["Mode"]["launchMode"]
    #         launchSecurity = config["Mode"]["launchSecurity"]
    #         if (launchSecurity):
    #             if (launchMode != "DEV"
    #             and launchMode != "PROD"
    #             and launchMode != "POSTMAN"):
    #                 raise ValueError("FATAL ERROR: Launch Mode Denied")
