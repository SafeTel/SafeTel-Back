##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Register
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
from datetime import datetime, timedelta
import jwt, config, uuid
import time

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail, isValidNumber

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Utils.MelchiorUtils import createDocumentForNewUser

UserDb = UserDB()

# validate Body for Login route
def UMRegisterBodyValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "email", "userName", "password", "customerInfos", "localization"]):
        return False
    if data["magicNumber"] != 42:
        return False
    if not isValidEmail(data["email"]):
        return False
    if not validateBody(
        data["customerInfos"],
        ["firstName", "lastName", "phoneNumber"]):
        return False
    if not isValidNumber(data["customerInfos"]["phoneNumber"]):
        return False
    if not validateBody(
        data["localization"],
        ["country", "region", "adress"]):
        return False
    return True

# Route to log in a user
class Register(Resource):
    def post(self):
        body = fquest.get_json()

        if not UMRegisterBodyValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        if UserDb.exists(body["email"]):
            return {
                'error': 'this email is already linked to an account'
            }, 400

        body["time"] = time.time()
        body["guid"] = str(uuid.uuid4())
        guid = body["guid"]

        UserDb.addUser(body)
        createDocumentForNewUser(guid)

        token = jwt.encode(
            {
                'guid': guid,
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            config.SECRET_KEY
        )
        return {
            'created': True,
            'userName': body["userName"],
            'token': token,
        }, 200
