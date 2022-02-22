##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitializeDevRessources
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Routes imports
from Routes.DevRessources.ClaimApiKeys import ClaimApiKeys
from Routes.DevRessources.RegisterAdminDev import RegisterAdminDev

def InitializeDevRessourcesRoutes(api):
    api.add_resource(ClaimApiKeys, "/devRessources/claimApiKey")
    api.add_resource(RegisterAdminDev, "/devRessources/register")
