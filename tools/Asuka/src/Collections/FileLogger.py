##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## File Logger
##


### LOGIC
# logging stl import
import os
import logging

class FileLogger():
    def __init__(self, loggerName= "FileLogger", filePath = "saves/", fileName = "database.json"):
        self.__FileHandler = None
        self.__FilePath = filePath
        self.__FileName = fileName

        self.Logger = None
        logger = logging.Logger(loggerName, logging.DEBUG)
        self.Logger = logger

        self.__CheckFilePath()
        self.__SetFileHandler()


    def __CheckFilePath(self):
        dir = os.path.join("./",self.__FilePath)
        if (not os.path.exists(dir)):
            os.mkdir(dir)

    def __SetFileHandler(self):
        if (self.__FileName == ""):
            return 
        self.__FileHandler = logging.FileHandler(self.__FilePath+self.__FileName)
        self.__FileHandler.setLevel(logging.DEBUG)
        self.__FileHandler.setFormatter(logging.Formatter('%(message)s'))

        self.Logger.addHandler(self.__FileHandler)


    def UpdateFileHandler(self, filePath, fileName):
        if (self.__FileHandler != None):
            self.Logger.removeHandler(self.__FileHandler)

        self.__FilePath = filePath
        self.__FileName = fileName
        self.__CheckFilePath()
        self.__SetFileHandler()

    def LoggingObjects(self, message: str, name: str, object: str):
        self.__CheckFilePath()
        self.Logger.info(message + " - " + name + " : " + object)

    def LoggingList(self, list: list) -> bool:
        self.__CheckFilePath()
        self.Logger.info(list)
        self.Logger.info("Test loggingList")
        return False
