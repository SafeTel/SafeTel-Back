##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## File Logger
##


### LOGIC
# logging stl import
import logging
# I/O stream
import sys

class FileLogger():
    __instance = None

    @classmethod
    def __init__(self, loggerName= "FileLogger", filePath = "logs/", fileName = "magi.log"):
        self.Logger = None

        if FileLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            logger = logging.Logger(loggerName, logging.DEBUG)
            self.Logger = logger
            self.__SetFileHandler(filePath+fileName)
            FileLogger.__instance = self

    @classmethod
    def LoggingObjects(self, message: str, name: str, object: str):
        self.Logger.info(message + " - " + name + " : " + object)

    @classmethod
    def __SetFileHandler(self, path):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

        self.Logger.addHandler(file_handler)


    @staticmethod
    def getInstance():
        if FileLogger.__instance == None:
            FileLogger()
        return FileLogger.__instance

