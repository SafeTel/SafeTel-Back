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
        self.Logger = None
        logger = logging.Logger(loggerName, logging.DEBUG)
        self.Logger = logger
        self.__FilePath = filePath
        self.__FileName = fileName
        self.__CheckFilePath()
        self.__SetFileHandler(filePath+fileName)

    def __SetFileHandler(self, path):
        self.__File_handler = logging.FileHandler(path)
        self.__File_handler.setLevel(logging.DEBUG)
        self.__File_handler.setFormatter(logging.Formatter('%(message)s'))

        self.Logger.addHandler(self.__File_handler)


    def UpdateFileHandler(self, path):
        self.Logger.removeHandler(self.__File_handler)

        self.__File_handler = logging.FileHandler(path)
        self.__File_handler.setLevel(logging.DEBUG)
        self.__File_handler.setFormatter(logging.Formatter('%(message)s'))

        self.Logger.addHandler(self.__File_handler)

    def __CheckFilePath(self):
        dir = os.path.join("./",self.__FilePath)
        if not os.path.exists(dir):
            os.mkdir(dir)

    def LoggingObjects(self, message: str, name: str, object: str):
        self.__CheckFilePath()
        self.Logger.info(message + " - " + name + " : " + object)

    def LoggingList(self, list: list) -> bool:
        self.__CheckFilePath()
        self.Logger.info(list)
        self.Logger.info("Test loggingList")
        return False
