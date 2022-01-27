##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## InitializesRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.Services.Tellows.GetTellows import GetTellows

def InitializeServicesRoutes(api):
    api.add_resource(GetTellows, "/services/tellows")
