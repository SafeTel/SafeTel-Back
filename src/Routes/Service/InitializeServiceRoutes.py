##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeServiceRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.Service.Tellows.GetTellows import GetTellows

def InitializeServiceRoutes(api):
    api.add_resource(GetTellows, "/service/tellows")
