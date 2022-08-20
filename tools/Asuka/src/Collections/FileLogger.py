##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## File Logger
##


### LOGIC
# logging stl import
import logging
# For Dir
import os
# For Json
import json
# For bson to load into json
from bson import json_util


class FileLogger():
    def __init__(self, loggerName= "FileLogger", filePath = "saves/", fileName = "save.json"):
        self.__FileHandler = None
        self.__LoggerName = loggerName
        self.__FilePath = filePath
        self.__FileName = fileName

        self.__InitLogger()
        self.__InitHandler()

    def __InitLogger(self):
        self.Logger = logging.Logger(self.__LoggerName, logging.DEBUG)

    def __InitHandler(self):
        self.__CheckFilePath()
        self.__SetFileHandler()

    def __CheckFilePath(self):
        if (self.__FilePath == ""):
            return
        self.CreateFolder(self.__FilePath)

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

    def UpdateFileHandlerFileName(self, fileName):
        self.UpdateFileHandler(self.__FilePath, fileName)

    def LoggingObjects(self, message: str, name: str, object: str):
        self.__CheckFilePath()
        self.Logger.info(message + " - " + name + " : " + object)

    def LoggingBsonIntoJson(self, data: list):
        self.__CheckFilePath()
        for elem in data:
            loadedBsonIntoJson = json.loads(json_util.dumps(elem))
            with open(self.__FilePath+self.__FileName, 'w') as f:
                json.dump(loadedBsonIntoJson, f, indent=4)

    @staticmethod
    def CreateFolder(filePath: str):
        if (filePath == ""):
            return
        dir = os.path.join("./",filePath)

        if (not os.path.exists(dir)):
            os.mkdir(dir)