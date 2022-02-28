##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Provider
##

### MODELS
# Role import
from Models.Logic.Shared.Roles import Roles

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

from Models.Logic.SharedJParent.JWTInfos import JWTInfos

class JWTConvert():
    def __init__(self):
        self.UserDb = UserDB()


    def Serialize(self, guid: str, role):
        if (guid == "" or guid is None):
            raise ValueError("The guid can't be empty or null.")
        if (role == None):
            raise ValueError("The role can't be none.")
        if (not Roles.HasValue(role)):
            raise ValueError("It should be an existing one.")

        return jwt.encode( {
                'guid': guid,
                'role': role,
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            os.getenv("SECRET_KEY")
        )


    def Deserialize(self, token: str):
        try:
            jwtInfos = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms='HS256')
        except Exception as e:
            return None

        infos = JWTInfos(jwtInfos["guid"], jwtInfos["role"], jwtInfos["exp"])
        curr_ts = time.time()

        if (curr_ts > infos.exp):
            return None

        if (not Roles.HasValue(infos.role) or self.UserDb.existByGUID(infos.guid) is False):
            return None
        if (infos.EvaluateModelErrors() != None):
            return None
        return infos


    def IsValid(self, token: str):
        try:
            data = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms='HS256')
        except Exception as e:
            return None

        exp = data['exp']
        curr_ts = time.time()

        if (curr_ts > exp):
            return False
        return True


    def SToRoles(self, s: str):
        if (s.lower() == "user"):
            return Roles.USER
        if (s.lower() == "dev"):
            return Roles.DEVELOPER
        if (s.lower() == "adming"):
            return Roles.ADMIN
        return None
