##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Magi
##

# Env values os import
import os

# Thread Imports
import logging
import threading

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from src.DataBases.Melchior import BlacklistDB
from src.DataBases.Melchior import WhitelistDB
from src.DataBases.Melchior import HistoryDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()
HistoryDb = HistoryDB()

# Params for $thread_function & launch API (Flask App)
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


    app.run(debug=False, host='0.0.0.0')
