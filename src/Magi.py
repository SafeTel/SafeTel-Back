##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Magi
##

### INFRA & LOGIC
# init Magi import
from MagiInit.InitMagi import InitMagi

### INFRA
# Flask import
from flask import Flask

### LOGIC
# import env vars
import os
# logging stl import
import logging


##########################
#### LAUNCHING SERVER ####
##########################

if __name__ == "__main__":

    InitializerMagi = InitMagi()
    MagiApp: Flask.app.Flask = InitializerMagi.Initialize()

    logging.warning("/!\ Be aware of the current git branch /!\\")
    logging.info("Launching Magi")

    serverPort = os.getenv("SERVER_PORT")
    MagiApp.run(debug=True, host="0.0.0.0", port=serverPort)
