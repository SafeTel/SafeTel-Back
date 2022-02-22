##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitializeServerManagementRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.ServerManagement.HealthCheck import HealthCheck

def InitializeServerManagementRoutes(api):
    api.add_resource(HealthCheck, "/server/healthCheck")
