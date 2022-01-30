##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## config
##

import os

# CLIENT & PASSWORD for MongoDB
client = os.getenv('DB_CLIENT', 'SafeTelBackEndUser')
password = os.getenv('DB_PASSWORD', 'aSEFTHUKOM1!')

# Melchior, Users DB
dbname = os.getenv('DB_USERS_NAME', 'Melchior')

# Casper, Devs DBs
dbnameCasper = os.getenv('DB_DEVELOPERS_NAME', 'Casper')
dbnameCasper02 = os.getenv('DB_SERVICES_NAME', 'Casper02')

# Secret Key encryption for JWT
SECRET_KEY = 'MankindsGreatestFearIsMankindItself'
