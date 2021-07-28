##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## MelchiorConfig
##

# Import db settings connextion
from config import client, password, dbname

URI_MELCHIOR = 'mongodb+srv://' + client + ':' + password + '@safetel-back-cluster.klq5k.mongodb.net/' + dbname + '?retryWrites=true&w=majority'
