##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeEmbededRessourcesRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.EmbededRessources.AvaibleUpdate import AvaiableUpdate

def InitializeEmbededRessourceRoutes(api):
    api.add_resource(AvaiableUpdate, "/embededRessources/update")
