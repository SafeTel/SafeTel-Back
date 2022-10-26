##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitMonitoring
##

### LOGIC
# os path management import
import os
# json stl import
import json
# flasgger framework import
import flask_monitoringdashboard as dashboard


# Init Magi's Swagger
class InitMonitoring():
    def __init__(self, path: str):
        self.__path = path


    def Initialize(self, App):
        if (not os.path.isfile(self.__path)):
            raise ValueError("FATAL ERROR: Environement Denied")

        dashboard.config.init_from(file=self.__path)

        dashboard.bind(App)

        return App
