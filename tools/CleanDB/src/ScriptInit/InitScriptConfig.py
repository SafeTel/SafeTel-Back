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
from MagiInit.InitServerConfig import InitServerConfig

class InitScriptConfig(InitServerConfig):
    def __init__(self):
        self.__IsValidConfig()
        self.__CheckEnvVars()
        self.__SecurityLaunchCheck()