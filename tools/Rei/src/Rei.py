##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Rei
##


#############################
### LOGING SETTINGS BEGIN ###
# Logs Imports
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Launching Rei...")
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend/wiki/Resume%3A-Tools")
###  LOGING SETTINGS END  ###
#############################

####################################
### Initiate Tool Config BEGIN ###
from InitToolConfig import InitToolConfig

logging.warning("--- /!\ Validating Environement /!\\ ----")
InitToolConfig()
logging.warning("---     Environement Validated      ----")
###  Initiate Tool Config END  ###
####################################

### To Perform the copy of a database
from ConfigDatabase import ConfigDatabase

if __name__ == "__main__":
    ConfigDatabase()