##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Provider
##

### MODELS
# Role import
from Logic.Models.Roles import Roles

### LOGIC
# jwt imports
from datetime import datetime, timedelta
import jwt
# Timestamp import
import time
# OS env import
import os

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB

class JWTConvert():
    def __init__(self):
        self.UserDb = UserDB()


    def Serialize(self, guid, role):
        if (guid == "" or guid is None):
            raise ValueError("The guid can't be empty or null.")
        if (role == None):
            raise ValueError("The role can't be none.")
        if (not Roles.has_value(role)):
            raise ValueError("It should be an existing one.")

        return jwt.encode( {
                'guid': guid,
                'role': role,
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            os.getenv("SECRET_KEY")
        )


    def Deserialize(self, token):
        try:
            jwtInfos = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms='HS256')
        except Exception as e:
            return None

        exp = jwtInfos['exp']
        curr_ts = time.time()

        if (curr_ts > exp):
            return None

        if (not Roles.has_value(jwtInfos['role']) or self.UserDb.existByGUID(jwtInfos['guid']) is False):
            return None
        return jwtInfos


    def IsValid(self, token):
        try:
            data = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms='HS256')
        except Exception as e:
            return None

        exp = data['exp']
        curr_ts = time.time()

        if (curr_ts > exp):
            return False
        return True


    def SToRoles(self, str):
        if (str.lower() == "user"):
            return Roles.USER
        if (str.lower() == "dev"):
            return Roles.DEVELOPER
        if (str.lower() == "adming"):
            return Roles.ADMIN
        return None
