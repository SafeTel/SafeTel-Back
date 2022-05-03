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
logging.info("You can find documentation on this repo: https://github.com/SafeTel/SafeTel-Doc-Backend")
###  LOGING SETTINGS END  ###
#############################


####################################
### Initiate Local DB BEGIN ###
logging.warning("--- /!\ Configuring Local DB depends on Launch mode  /!\\ ----")
from Init.InitLocalServer import InitLocalServer
InitLocalServer()
logging.warning("---     Local DB Configuration Ended      ----")

###  Initiate Local DB END  ###
####################################