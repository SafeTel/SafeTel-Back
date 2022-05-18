##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitSwagger
##

### LOGIC
# os path management import
import os
# json stl import
import json
# flasgger framework import
from flasgger import Swagger

# Init Magi's Swagger
class InitSwagger():
    def __init__(self, path: str):
        self.__path = path


    def Initialize(self, App):
        if (not os.path.isfile(self.__path)):
            raise ValueError("FATAL ERROR: Environement Denied")

        SwaggerConfig = []

        with open(self.__path) as JsonFile:
            SwaggerConfig = json.load(JsonFile)

        Swagger(App, SwaggerConfig)

        return App
