##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## UpdateEmail
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail
from Routes.Utils.JWTProvider.Provider import DeserializeJWT

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Melchior.InternalUtils.DataWorker import UpdateAccountEmail

UserDb = UserDB()

# validate Body for Update email route
def UMUpdateEmailBodyValidation(data):
    if not validateBody(
        data,
        ["token", "email"]):
        return False
    if not isValidEmail(data["email"]):
        return False
    return True

# Route to update the email of an account from an auth user
class UpdateEmail(Resource):
    def post(self):
        body = fquest.get_json()

        if not UMUpdateEmailBodyValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        data = DeserializeJWT(body["token"])
        if data is None:
            return {
                'error': 'bad_token'
            }, 400

        result = UserDb.getUserByGUID(data['guid'])
        if result is None:
            return {
                'error': 'bad_token'
            }, 400

        UpdateAccountEmail(UserDb.Users, data['guid'], body['email'])

        return {
            'updated': not UserDb.exists(result['email'])
        }, 200

