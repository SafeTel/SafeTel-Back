##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitEndpoints
##

### LOGIC
import logging

### INFRA
# Init Endpoints Account import
from Endpoints.Account.InitAccountEndpoints import InitAccountEndpoints
# Init Endpoints Authentification import
from Endpoints.Authentification.InitAuthEndpoints import InitAuthentificationEndpoints
# Init Endpoints Engine import
from Endpoints.Engine.InitEngineEndpoints import InitEngineEndpoints
# Init Endpoints InternalDev import
from Endpoints.InternalDev.InitInternalDevEndpoints import InitInternalDevEndpoints

class InitEndpoints():
    def __init__(self, Api):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        self.__InitEndpoints(Api)
        logging.info("All endpoints initialized")


    def __InitEndpoints(self, Api):
        logging.info("Account endpoints initialization...")
        InitAccountEndpoints(Api)
        logging.info("Account endpoints initialized...")

        logging.info("Authentification endpoints initialization...")
        InitAuthentificationEndpoints(Api)
        logging.info("Authentification endpoints initialized...")

        logging.info("Engine endpoints initialization...")
        InitEngineEndpoints(Api)
        logging.info("Engine endpoints initialized...")

        logging.info("InternalDev endpoints initialization...")
        InitInternalDevEndpoints(Api)
        logging.info("InternalDev endpoints initialized...")
