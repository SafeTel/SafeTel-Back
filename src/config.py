##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## config
##

from ast import pattern
import os
import re
import json

if  ('DB_CLIENT' in os.environ) == False            \
    or ('DB_PASSWORD'in os.environ) == False        \
    or ('DB_USERS_NAME'in os.environ) == False      \
    or ('DB_DEVELOPERS_NAME'in os.environ) == False \
    or ('URI_USERS_DB'in os.environ) == False       \
    or ('URI_DEVELOPERS_DB'in os.environ) == False:

    # Reading the config.json file to load the right env file
    json_file = open('config.json', 'r')
    config_json_data = json.load(json_file)

    deployement_mode = config_json_data['deployement_mode']
    env_config_file = config_json_data['env_config_file']

    json_file.close()

    # Loading right .env file matching the deployement mode
    env_file = open(env_config_file, 'r')
    file_content_lines = env_file.readlines()

    regex_for_env = re.compile(r'([A-Z_]+)=([a-zA-Z0-9!\/+:@\-\.?=&]+)')
    for line in file_content_lines:
        matches = regex_for_env.finditer(line) # find matches from line using regex_for_env
        for match in matches:
            env_identifier = match.group(1)
            env_value = match.group(2)
            if env_identifier != None and env_value != None:
                os.environ[env_identifier] = env_value
    env_file.close()

# CLIENT & PASSWORD for MongoDB
client = os.getenv('DB_CLIENT', 'SafeTelBackEndUser')
password = os.getenv('DB_PASSWORD', 'aSEFTHUKOM1!')

# Melchior, Users DB
dbname = os.getenv('DB_USERS_NAME', 'Melchior')

# Casper, Devs DBs
dbnameCasper = os.getenv('DB_DEVELOPERS_NAME', 'Casper')
dbnameCasper02 = os.getenv('DB_SERVICES_NAME', 'Casper02')

URI_MELCHIOR = os.getenv('URI_USERS_DB', 'mongodb+srv://' + client + ':' + password + '@safetel-back-cluster.klq5k.mongodb.net/' + dbname + '?retryWrites=true&w=majority')

# Secret Key encryption for JWT
SECRET_KEY = 'MankindsGreatestFearIsMankindItself'
