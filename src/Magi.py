##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Magi
##

# Thread Imports
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Launching Magi...")
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend")

# Network Imports
import requests
import os
import config
from flask import Flask
from Routes.Utils.JWTProvider.Roles import Roles
from flask_restful import Api


# ---
# import Sentry
import sentry_sdk
# Sentry integration
sentry_sdk.init(
    "https://840739ef53034860b515d400dc4b6219@o1036766.ingest.sentry.io/6004367",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
logging.info("Connected to sentry")


# ---
# Flask initialitation
app = Flask(__name__)
app.debug = True
api = Api(app)


# ---
## Initialization of routes imports

# Initialize User Routes
from Routes.UserManagement.InitializeUserManagementRoutes import InitializeUserManagementRoutes
from Routes.UserLists.InitializeUserListsRoutes import InitializeUserListsRoutes

InitializeUserManagementRoutes(api)
InitializeUserListsRoutes(api)

logging.info("Routes initialized - User Lists")

# Initialize s Routes
from Routes.Services.InitializeServicesRoutes import InitializeServicesRoutes
InitializeServicesRoutes(api)

logging.info("Routes initialized - Services")

# Initialize server ressources routes
from Routes.ServerManagement.InitializeServerManagementRoutes import InitializeServerManagementRoutes
InitializeServerManagementRoutes(api)

logging.info("Routes initialized - Server Management")

# Initialize embeded ressources routes
from Routes.EmbededRessources.InitializeEmbededRessourcesRoutes import InitializeEmbededRessourceRoutes
InitializeEmbededRessourceRoutes(api)

logging.info("Routes initialized - Embeded Ressources")

# Initialize dev ressources routes
from Routes.DevRessources.InitializeDevRessources import InitializeDevRessourcesRoutes
InitializeDevRessourcesRoutes(api)

logging.info("Routes initialized - Dev Ressources")


# ---
# Logs imports
import socket


from flask_cors import CORS
CORS(app)

if __name__ == "__main__":
    logging.warning("/!\ You are starting the server connected with Mongo DB, this is a shared DB /!\\")
    logging.warning("/!\ Be aware of the current git branch DEV or PROD /!\\")

    env_port = os.getenv('SERVER_PORT', '2407')

    logging.info("Launching API on : 0.0.0.0:2407")
    app.run(debug=True, host='0.0.0.0', port=env_port)
