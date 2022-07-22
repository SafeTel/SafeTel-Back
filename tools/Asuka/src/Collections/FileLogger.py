##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## File Logger
##


### LOGIC
# logging stl import
import logging

class FileLogger():
    def __init__(self, loggerName= "FileLogger", filePath = "saves/", fileName = "database.json"):
        self.Logger = None
        logger = logging.Logger(loggerName, logging.DEBUG)
        self.Logger = logger
        self.__SetFileHandler(filePath)

    def LoggingObjects(self, message: str, name: str, object: str):
        self.Logger.info(message + " - " + name + " : " + object)

    def __SetFileHandler(self, path):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

        self.Logger.addHandler(file_handler)