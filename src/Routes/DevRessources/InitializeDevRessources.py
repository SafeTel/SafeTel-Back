##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeDevRessources
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

from Routes.DevRessources.ClaimApiKeys import ClaimApiKeys

def InitializeDevRessourcesRoutes(api):
    api.add_resource(ClaimApiKeys, "/devRessources/claimApiKey")
