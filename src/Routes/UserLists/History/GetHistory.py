##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetHistory
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# DB import
from DataBases.Melchior.HistoryDB import HistoryDB

# Utils import
from Routes.Utils.JWTProvider.Provider import DeserializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

HistoryDb = HistoryDB()

# Route to get the whitelist of the user
class GetHistory(Resource):
    def get(self):
        data = DeserializeJWT(request.args["token"], Roles.USER)
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        guid = data['guid']
        return {
            'History': HistoryDb.getHistoryForUser(guid)["History"]
        }, 200
