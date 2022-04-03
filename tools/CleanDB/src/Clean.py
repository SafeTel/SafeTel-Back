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

#######################################
### IMPORTING FILE FROM MAGI BEGIN ###

# Import Class src/MagiInit/InitServerConfig
from os import path
import sys
sys.path.append(path.abspath('../../../../src/MagiInit/InitServerConfig.py'))

### IMPORTING FILE FROM MAGI END   ###
#######################################


####################################
### Initiate Server Config BEGIN ###
logging.warning("--- /!\ Validating Environement /!\\ ----")

# from ScriptInit.InitScriptConfig import InitScriptConfig
# InitScriptConfig()
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

from DBClean import DBClean


############################
#### LAUNCHING CLEANING ####
############################

if __name__ == "__main__":
    Client = pymongo.MongoClient(os.getenv("DB_URI_"))
    DBName = os.getenv("DB_MELCHIOR")
    DBMelchior = Client[DBName]
    MongoDBClean = DBClean(Client, DBMelchior)

    # MongoDBClean.setDatabasesCollectionPair()

    schedule.every(2).seconds.do(MongoDBClean.run)

    schedule.every().day.at("10:00:42").do(MongoDBClean.run)

    while True:
        schedule.run_pending()
        time.sleep(1)



    # while True:



    #     Blacklist = DBMelchior['Blacklist']
    #     History = DBMelchior['History']
    #     User = DBMelchior['User']
    #     Whitelist = DBMelchior['Whitelist']

    #     DBName = os.getenv("DB_CASPER")
    #     DBCasper = Client[DBName]

    #     ApiKeyLog = DBCasper['']
    #     Contributors = DBCasper['']

    #     DBName = os.getenv("DB_CASPER_02")
    #     DBCasperTwo = Client[DBName]

    #     DBName = os.getenv("DB_BALTHASAR")
    #     DBBalthasar = Client[DBName]


    # MongoDB.delete_many({})