##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Magi
##

# Thread Imports
import logging

# Network Imports
import requests
from flask import Flask
from Routes.Utils.JWTProvider.Roles import Roles
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# Initialization of routes imports
from Routes.UserManagement.InitializeUserManagementRoutes import InitializeUserManagementRoutes
from Routes.UserLists.InitializeUserListsRoutes import InitializeUserListsRoutes
from Routes.ServerManagement.InitializeServerManagementRoutes import InitializeServerManagementRoutes

InitializeUserManagementRoutes(api)
InitializeUserListsRoutes(api)
InitializeServerManagementRoutes(api)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    app.run(debug=False, host='0.0.0.0', port='2407')
