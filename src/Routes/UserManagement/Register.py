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
import uuid
import time

# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail, isValidNumber
from Routes.Utils.JWTProvider.Provider import SerializeJWT
from Routes.Utils.JWTProvider.Roles import Roles

# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError

# Password encription import
from Routes.Utils.PWDSerialiazer.Serializer import SerializePWD

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB
from DataBases.Utils.MelchiorUtils import createDocumentForNewUser

UserDb = UserDB()

# validate Body for Register route
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

# Route to Register a user
class Register(Resource):
    def post(self):
        body = fquest.get_json()
        if not UMRegisterBodyValidation(body):
            return BadRequestError("bad request"), 400

        if UserDb.exists(body["email"]):
            return BadRequestError("this email is already linked to an account"), 400

        body["time"] = time.time()
        body["guid"] = str(uuid.uuid4())
        guid = body["guid"]
        body["password"] = SerializePWD(body["password"])

        UserDb.addUser(body, Roles.USER)
        createDocumentForNewUser(guid)

        return {
            'created': True,
            'userName': body["userName"],
            'token': SerializeJWT(guid, Roles.USER)
        }, 200
