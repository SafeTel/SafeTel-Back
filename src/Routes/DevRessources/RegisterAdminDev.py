##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## RegisterAdminDev
##

# Network imports
from flask import request as fquest
from flask.globals import request
from flask_restful import Resource

# utils imports
import uuid
import time

# Utils check imports
from Routes.Utils.JWTProvider.Provider import SerializeJWT
from Routes.Utils.Request import validateBody
from Routes.Utils.JWTProvider.Roles import Roles

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Utils.MelchiorUtils import createDocumentForNewUser

# DB imports
from DataBases.Casper.ApiKeys import ApiKeyLogDB

UserDb = UserDB()

ApiKeyLogDb = ApiKeyLogDB()

def DRRegisterAdminDevValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "apiKey", "role", "registration"]):
        return False
    if not validateBody(
        data["registration"],
        ["userName", "email", "password"]):
        return False
    if data["magicNumber"] != 84:
        return False
    return True

class RegisterAdminDev(Resource):
    def post(self):
        body = fquest.get_json()

        if not DRRegisterAdminDevValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        if (not ApiKeyLogDb.isValidApiKey(body['apiKey'])):
            return {
                'error': 'apiKey is not valid'
            }

        registration = body['registration']

        if UserDb.exists(registration["email"]):
            return {
                'error': 'this email is already linked to an account'
            }, 400

        create_ts = time.time()
        guid = str(uuid.uuid4())

        registration['guid'] = guid
        registration['ts'] = create_ts

        role = Roles.USER

        if (body['role'] == 'admin'):
            role = Roles.ADMIN
        elif (body['role'] == 'dev'):
            role = Roles.DEVELOPER
        else:
            return {
                'error': 'not a valid role'
            }, 400

        UserDb.addUser(registration, role)
        createDocumentForNewUser(guid)

        return {
            'created': True,
            'userName': registration['userName'],
            'token': SerializeJWT(guid, role)
        }
