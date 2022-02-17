##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## config
##

### LOGIX
import os
import json
from pathlib import Path

### INFRA
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class InitiateServerConfig():
    def __init__(self):
        self.__IsValidConfig()
        self.__CheckEnvVars()
        self.__Ping()
        self.__SecurityLaunchCheck()


    def __IsValidConfig(self):
        if (not os.path.isfile("config.json")):
            raise ValueError("FATAL ERROR: Environement denied.")
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            if (["Mode"]["launchMode"] not in config
            or ["Mode"]["launchSecurity"] not in config
            or ["Mode"]["message"] not in config
            or ["MandatoryEnvVars"] not in config):
                raise ValueError("FATAL ERROR: Configuration denied.")

    def __ValudateConfig(self, json, keys):
        for i in keys:
            if not i in json:
                return False
            else:
                if json[i] == "":
                    return False
        return True


    def __CheckEnvVars(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            for mandatoryEnvVar in config["MandatoryEnvVars"]:
                if (mandatoryEnvVar in os.environ) == False:
                    raise ValueError("FATAL ERROR: Environement denied.")


    def __Ping(self):
        httpClient = HttpClient()
        pingUri = os.getenv("PING_URI")
        if httpClient.IsUp(pingUri) == None:
            raise ValueError("FATAL ERROR: Environement denied.")


    def __SecurityLaunchCheck(self):
        with open("config.json", 'r') as jsonFile:
            config = json.load(jsonFile)
            launchMode = config["Mode"]["launchMode"]
            launchSecurity = config["Mode"]["launchSecurity"]
            if (launchSecurity):
                if (launchMode != "DEV"
                or launchMode != "PROD"
                or launchMode != "POSTMAN"):
                    raise ValueError("FATAL ERROR: Configuration denied.")
                launchMode = launchMode.lower()
                branch = self.__GetBranchName()
                if (launchMode != branch):
                    raise ValueError("FATAL ERROR: Launch Mode denied.")


    def __GetBranchName():
        head_dir = Path(".") / ".git" / "HEAD"
        with head_dir.open("r") as f: content = f.read().splitlines()
        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]


