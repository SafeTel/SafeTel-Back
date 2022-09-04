##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Asuka
##


#############################
### LOGING SETTINGS BEGIN ###
# Logs Imports
import logging


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Launching Asuka...")
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend/wiki/Resume%3A-Tools")
###  LOGING SETTINGS END  ###
#############################

####################################
### Initiate Tool Config BEGIN ###
logging.warning("--- /!\ Validating Environement /!\\ ----")

from InitToolConfig import InitToolConfig
InitToolConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Tool Config END  ###
####################################

### To Perform the copy of a database

# For argv
import sys
# For Running DBSave
from RunDBSave import runDBSave


if (__name__ == "__main__"):
    runDBSave(sys.argv)
