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
    def __init__(self, loggerName= "FileLogger", filePath = "logs/", fileName = "magi.log"):
        logger = logging.Logger(loggerName, logging.DEBUG)
        self.Logger = logger
        self.__SetFileHandler(filePath+fileName)


    def __SetFileHandler(self, path):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

        self.Logger.addHandler(file_handler)

