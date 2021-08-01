##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeUserManagementRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.UserManagement.Register import Register

def InitializeUserManagementRoutes(api):
    api.add_resource(Register, "/user/register")
