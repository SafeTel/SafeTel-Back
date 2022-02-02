##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Provider
##

# Role import
from Routes.Utils.JWTProvider.Roles import Roles

# jwt config imports
from datetime import datetime, timedelta
import jwt, config

# Melchior DB imports
from DataBases.Melchior.UserDB import UserDB

# Timestamp import
import time

UserDb = UserDB()

def SerializeJWT(guid, role):
    if (guid == "" or guid is None):
        raise ValueError("guid can't be empty or null.")
    if (role == None):
        raise ValueError("role can't be none.")

    return jwt.encode({
            'guid': guid,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        config.SECRET_KEY
    )

def DeserializeJWT(str, role):
    if (not VerifyJWT(str)):
        return None

    data = jwt.decode(jwt=str, key=config.SECRET_KEY, algorithms='HS256')

    if (not Roles.has_value(data['role']) or UserDb.existByGUID(data['guid']) is False):
        return None
    if (not data['role'] == role):
        return None
    return data

def IsValidJWT(jwt):
    if (VerifyJWT(jwt) == False):
        return None
    data = DeserializeJWT(jwt, Roles.USER)
    exp = data['exp']
    curr_ts = time.time()
    if (curr_ts < exp):
        return True
    return False

def VerifyJWT(str):
    if (str == None or len(str) < 10):
        return False
    return True

def StrToRole(str):
    if (str == "admin"):
        return Roles.ADMIN
    if (str == "developer"):
        return Roles.DEVELOPER
    if (str == "user"):
        return Roles.USER
    return None
