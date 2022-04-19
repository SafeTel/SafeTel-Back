##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# Clean Database
##

#############################
### LOGING SETTINGS BEGIN ###
# Logs Imports
import logging
from multiprocessing.connection import Client

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Launching Clean of DEV mongoDB...")
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend")
###  LOGING SETTINGS END  ###
#############################

####################################
### Initiate Server Config BEGIN ###
logging.warning("--- /!\ Validating Environement /!\\ ----")

from ScriptInit.ScriptConfig import ScriptConfig
from ScriptInit.AmaneConfig import AmaneConfig
import sys

if len(sys.argv) == 2:
    if sys.argv[1] == '--force-now':
        AmaneConfig()
    elif sys.argv[1] == "--force":
        AmaneConfig()
ScriptConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Server Config END  ###
####################################

### INFRA
# Client mongo db import
import pymongo

### LOGIC
# env var import
import os
# Schedule events
import schedule
import time
# Signals
import signal

from DBClean import DBClean

############################
#### LAUNCHING CLEANING ####
############################

def handler(signum, frame):
    logging.info('Raising signal to stop Amane tool')
    sys.exit(1)

if __name__ == "__main__":
    Client = pymongo.MongoClient(os.getenv("DB_URI"))

    MongoDBClean = DBClean(Client)
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_MELCHIOR"), ['Blacklist', 'History', 'User', 'Whitelist'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_CASPER"), ['ApiKeyLog', 'Contributors'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_CASPER_02"), ['GoogleServices'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_BALTHASAR"), ['Boxes', 'UnclaimedBoxes'])

    if len(sys.argv) == 2:
        if sys.argv[1] == '--force-now':
            MongoDBClean.run()
            exit(0)
        elif sys.argv[1] == '--force':
            signal.signal(signal.SIGINT, handler)
            schedule.every().day.at("10:00:42").do(MongoDBClean.run)
    else:
        signal.signal(signal.SIGINT, handler)
        schedule.every().day.at("10:00:42").do(MongoDBClean.run)

    while True:
        schedule.run_pending()
        time.sleep(300)
