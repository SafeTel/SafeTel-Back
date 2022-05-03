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

### To Perform the copy of a database
from Init.InitDatabase import InitDatabase

if __name__ == "__main__":
    logging.warning("--- /!\ Configuring DB /!\\ ----")
    InitDatabase()
    logging.warning("--- DB Configuration Ended  ----")