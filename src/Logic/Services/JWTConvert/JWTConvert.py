##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Provider
##

### MODELS
# Role import
from Models.Logic.Shared.Roles import Roles
# JwtInfos Model import
from Models.Logic.SharedJParent.JWTInfos import JWTInfos

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


    def Serialize(self, guid: str, role: Roles):
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

        Infos = JWTInfos(jwtInfos["guid"], self.__StrToRoles(jwtInfos["role"]), int(jwtInfos["exp"]))
        curr_ts = time.time()

        if (curr_ts > Infos.exp):
            return None

        if (not Roles.HasValue(Infos.role) or self.UserDb.existByGUID(Infos.guid) is False):
            return None
        if (Infos.EvaluateModelErrors() != None):
            return None
        return Infos


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


    def __StrToRoles(self, s: int):
        if (s == 1):
            return Roles.ADMIN
        if (s == 2):
            return Roles.DEVELOPER
        if (s == 3):
            return Roles.USER
        return None
