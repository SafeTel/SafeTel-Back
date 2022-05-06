##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Magi
##

# TODO: Clean Magi.py splitting by Services on MagiInit Folder

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
from MagiInit.InitServerConfig import InitServerConfig

logging.warning("--- /!\ Validating Environement /!\\ ----")
InitServerConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Server Config END  ###
####################################


#######################################
### Initiate Server Condition BEGIN ###
from MagiInit.InitServerCondition import InitServerCondition

logging.warning("--- /!\ Validating Conditions /!\\ ----")
InitServerCondition()
logging.warning("---     Conditions Validated      ----")
###  Initiate Server Condition END  ###
#######################################


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


#######################
### API SETUP BEGIN ###
# Network Imports
import os
from flask import Flask
from flask_restful import Api

from flask_cors import CORS

# Flask initialitation
app = Flask(__name__)

app.debug = True
api = Api(app)

# CORS initialisation
CORS(app)

# Endpoints Initialization
from MagiInit.InitEndpoints import InitEndpoints
InitEndpoints(api)
###  API SETUP END  ###
#######################


#############################
### SWAGGER SERVICE BEGIN ###
import json
from flasgger import Swagger

if (not os.path.isfile("configuration/SwaggerConfig.json")):
    raise ValueError("FATAL ERROR: Environement Denied")

SwaggerConfig = []

with open('configuration/SwaggerConfig.json') as JsonFile:
    SwaggerConfig = json.load(JsonFile)

swagger = Swagger(app, SwaggerConfig)

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
