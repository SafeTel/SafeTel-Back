##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Magi
##


#############################
### LOGING SETTINGS BEGIN ###
# Logs Imports
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Launching Magi...")
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend")
###  LOGING SETTINGS END  ###
#############################


####################################
### Initiate Server Config BEGIN ###
logging.warning("--- /!\ Validating Environement /!\\ ----")
from MagiInit.InitServerConfig import InitServerConfig
InitServerConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Server Config END  ###
####################################


###############################
### EXTERNAL SERVICES BEGIN ###
# Sentry integration
import sentry_sdk
sentry_sdk.init(
    "https://840739ef53034860b515d400dc4b6219@o1036766.ingest.sentry.io/6004367",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
logging.info("Connected to sentry")
###  EXTERNAL SERVICES END  ###
###############################


###################
### INFRA BEGIN ###
# Network Imports
import os
from flask import Flask
from flask_restful import Api

# Flask initialitation
app = Flask(__name__)

app.debug = True
api = Api(app)

# CORS initialisation
from flask_cors import CORS
CORS(app)

# Endpoints Initialization
from MagiInit.InitEndpoints import InitEndpoints
InitEndpoints(api)
###  INFRA END  ###
###################


#############################
### SWAGGER SERVICE BEGIN ###
from flasgger import Swagger

''' swagger_config = {
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, DELETE, PATCH"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "endpoint": '',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
} '''

swagger_config = {
    "swagger_version": "2.0",
    "title": "Magi",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "static_url_path": "/flasgger_static",
    "headers": [
    ],
    "specs": [
        {
            "version": "BETA 1.0",
            "title": "Magi API",
            "endpoint": 'v1_spec',
            "description": 'Magi is SafeTel\'s server, documentation: https://github.com/SafeTel/SafeTel-Doc-Backend/wiki',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True   # all in
        }
    ]
}


swagger = Swagger(app, config=swagger_config)
###  SWAGGER SERVICE END  ###
#############################


##########################
#### LAUNCHING SERVER ####
##########################

if __name__ == "__main__":
    logging.warning("/!\ You are starting the server connected with Mongo DB, this is a shared DB /!\\")
    logging.warning("/!\ Be aware of the current git branch DEV or PROD /!\\")

    serverPort = os.getenv("SERVER_PORT")

    logging.info("Launching Magi.")
    app.run(debug=True, host="0.0.0.0", port=serverPort)
