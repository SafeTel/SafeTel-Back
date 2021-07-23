##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Login
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
from datetime import datetime, timedelta
import jwt, config

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail, isValidNumber

# Melchior DB imports
from DataBases.Melchior import UserDB
from DataBases.Utils.MelchiorUtils import createDocumentForNewUser

UserDb = UserDB()

# validate Body for Login route
def UMLoginBodyValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "email", "password"]):
        return False
    if data["magicNumber"] != 42:
        return False
    return True

# Route to log in a user
class Login(Resource):
    def post(self):
        body = fquest.get_json()

        if not UMLoginBodyValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        user = UserDb.getUser(body["email"])

        if user == None:
            return {
                'error': 'this email is not linked to an account'
            }, 400

        token = jwt.encode(
            {
                'guid': user["guid"],
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            config.SECRET_KEY
        )
        return {
            'userName': user["userName"],
            'token': token,
        }, 200