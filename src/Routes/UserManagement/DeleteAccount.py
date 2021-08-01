##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## DeleteAccount
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
from datetime import datetime, timedelta
import jwt, config, time

# Utils check imports
from Routes.Utils.Request import validateBody

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Utils.MelchiorUtils import deleteDocumentForUser, isDeletedDocumentForUser

UserDb = UserDB()

# validate Body for DeleteAccount route
def UMDeleteAccountBodyValidation(data):
    if not validateBody(
        data,
        ["token", "userName"]):
        return False
    return True

# Route to delete an account from an auth user
class DeleteAccount(Resource):
    def delete(self):
        body = fquest.get_json()

        if not UMDeleteAccountBodyValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        data = jwt.decode(jwt=body['token'], key=config.SECRET_KEY, algorithms='HS256')

        result = UserDb.getUserByGUID(data['guid'])
        if result is None:
            return {
                'error': 'bad_token'
            }, 400

        if result["userName"] != body["userName"]:
            return {
                'error': 'manual security check failed'
            }, 400

        deleteDocumentForUser(data['guid'])

        if isDeletedDocumentForUser(data['guid']):
            UserDb.deleteUser(data['guid'])

        # time.sleep(10)
        # TODO: see why mongodb is so much to delete documents

        return {
            'deleted': UserDb.exists(result['email'])
        }, 200
