##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Init Save File Parameters
##

### LOGIC
# For Getenv
import logging
import os
# datetime
from datetime import datetime

class InitSaveFileParameters:
    def __init__(self):
        self.__InitFilepath()

    def __InitFilepath(self):
        self.__Mode = os.getenv("MODE")
        self.__Date = datetime.utcnow().strftime("%Y-%m-%d-T%H_%M_%SZ")
        self.__Filepath= "saves/"+self.__Mode+"-"+self.__Date

    def GetFilePath(self):
        return self.__Filepath