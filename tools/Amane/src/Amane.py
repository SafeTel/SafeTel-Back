##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# Clean Database
##

from RunDBClean import runDBClean

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

from ScriptInit.AmaneConfig import AmaneConfig
import sys

if len(sys.argv) == 2:
    if sys.argv[1] == "--force-now":
        AmaneConfig(isForceLaunch=True)
else:
    AmaneConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Server Config END  ###
####################################

############################
#### LAUNCHING CLEANING ####
############################

if __name__ == "__main__":
    runDBClean(sys.argv)
