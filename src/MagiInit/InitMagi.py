##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitMagi
##

### INFRA
# Sentry Init import
from MagiInit.ExternalServices.InitSentry import InitSentry
# Core Init import
from MagiInit.InitCore import InitCore
# Network Configuration import
from MagiInit.InternalInit.InitMagiNetwork import InitMagiNetwork
# Endpoints Init import
from MagiInit.InternalInit.InitEndpoints import InitEndpoints
# Flask import
from flask import Flask
# Restfull api import
from flask_restful import Api

### LOGIC
# logging stl import
import logging
# Magi Configuration import
from MagiInit.InternalInit.InitMagiConfig import InitMagiConfig
# Swagger Init import
from MagiInit.ExternalServices.InitSwagger import InitSwagger


# Initialize Magi
class InitMagi():
    def __init__(self):
        self.__InitLogs()
        logging.info("Launching Magi")
        logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend")

        self.__InitSentry = InitSentry()
        InitMagiConfig()
        InitMagiNetwork()
        self.__InitCore = InitCore()
        self.__InitSwagger = InitSwagger

        self.__MagiApp: Flask.app.Flask = None
        self.__MagiApi: Api.Api = None

    ### PUBLIC

    def Initialize(self, debug: bool = True):
        self.__LaunchSentry()
        self.__InitializeCore()
        self.__InitializeEndpoints()
        self.__InitializeSwagger()
        return self.__MagiApp


    ### PRIVA1TE

    def __InitLogs(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


    def __LaunchSentry(self):
        self.__InitSentry.Initialize()


    def __InitializeCore(self):
        MagiApp, MagiApi = self.__InitCore.Initialize()
        self.__MagiApp = MagiApp
        self.__MagiApi = MagiApi


    def __InitializeEndpoints(self):
        InitEndpoints(self.__MagiApi)


    def __InitializeSwagger(self):
        self.__MagiApp = self.__InitSwagger.Initialize(self.__MagiApp)
