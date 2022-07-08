##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitCore
##

### INFRA
# Flask import
from flask import Flask
# Restfull api import
from flask_restful import Api
# CORS for flask import
from flask_cors import CORS

### LOGIC
# loigging stl import
import logging


# Iniutialize Magi App & Api
class InitCore():
    def __init__(self):
        logging.info("Magi App & Api Initialization")

    ### PUBLIC

    def Initialize(self, debug: bool = True):
        MagiApp = Flask(__name__)
        
        MagiApp.debug = debug # TODO: Put this param into the config.jsoin
        MagiApi = Api(MagiApp)
        logging.info("Magi App & Api Initialized")

        MagiApp = self.__InitCORS(MagiApp)
        logging.info("Magi App CORS Applied")

        return MagiApp, MagiApi

    ### PRIVATE

    def __InitCORS(self, MagiApp):
        CORS(MagiApp)
        return MagiApp
