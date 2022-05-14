##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EmbeddedJWTConvert
##

##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Provider
##

### MODELS
# Role import
from Models.Logic.Shared.Roles import Roles
# JwtInfos Model import
from Models.Logic.SharedJParent.JWTEmbeddedInfos import JWTEmbeddedInfos

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


class JWTConvertEmbedded():
    def __init__(self, expiration = 24):
        self.__UserDb = UserDB()
        self.__SECRET_KEY = os.getenv("SECRET_KEY")
        self.__expiration = expiration


    ### PUBLIC

    def Serialize(self, guid: str, boxid: str):
        if (guid == "" or guid is None):
            raise ValueError("The guid can't be empty or null.")

        return jwt.encode( {
                "guid": guid,
                "boxid": boxid,
                "exp": datetime.utcnow() + timedelta(hours=self.__expiration)
            },
            self.__SECRET_KEY
        )


    def Deserialize(self, token: str):
        JwtInfos = self.__DecodeJWT(token)
        if (JwtInfos is None):
            return None

        Infos = JWTEmbeddedInfos(
            JwtInfos["guid"],
            JwtInfos["boxid"],
            int(JwtInfos["exp"])
        )

        if (not self.__IsValidExp(Infos.exp)
            or self.__UserDb.existByGUID(Infos.guid) is False
            or Infos.EvaluateModelErrors() != None):
            return None
        return Infos


    ### PRIVATE

    def __DecodeJWT(self, token: str):
        try:
            JwtInfos = jwt.decode(jwt=token, key=self.__SECRET_KEY, algorithms='HS256')
        except Exception as e:
            return None
        return JwtInfos


    def __IsValidExp(self, exp: int):
       return time.time() < exp
