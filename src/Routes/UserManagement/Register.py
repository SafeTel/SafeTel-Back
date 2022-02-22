##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Register
##

### LOGIC
# Utils check imports
from Routes.Utils.Request import validateBody
from Routes.Utils.Types import isValidEmail, isValidNumber
from Logic.Models.Roles import Roles
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Request Error
from Routes.Utils.RouteErrors.Errors import BadRequestError
# Password encription import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert

### INFRA
# Network imports
from flask import request as fquest
from flask_restful import Resource
import uuid
import time
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.UserListsUtils import UserListsUtils


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

        pwdConv = PWDConvert()

        body["time"] = time.time()
        body["guid"] = str(uuid.uuid4())
        guid = body["guid"]
        body["password"] = pwdConv.Serialize(body["password"])

        UserDb.addUser(body, Roles.USER)

        ULUtils = UserListsUtils()
        ULUtils.CreateUserLists(guid)

        jwtConv = JWTConvert()
        return {
            'created': True,
            'userName': body["userName"],
            'token': jwtConv.Serialize(guid, Roles.USER)
        }, 200
