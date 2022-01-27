##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## config
##

import os

client = os.getenv('DB_CLIENT', 'SafeTelBackEndUser')
password = os.getenv('DB_PASSWORD', 'aSEFTHUKOM1!')
dbname = os.getenv('DB_USERS_NAME', 'Melchior')
dbnameCasper = os.getenv('DB_DEVELOPERS_NAME', 'Casper')
SECRET_KEY = 'MankindsGreatestFearIsMankindItself'
