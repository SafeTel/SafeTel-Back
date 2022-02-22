##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## HealthCheckService
##

# Network imports
import imp
from flask import request as fquest
from flask_restful import Resource

# Client mongo db import
from flask.globals import request
import pymongo

# Health Check imports
from healthcheck import HealthCheck as HealthCheckFromPackage
from healthcheck import EnvironmentDump

# Utils imports
import json

# JWT imports
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

import os

class HealthCheckService():
    def __init__():
        
