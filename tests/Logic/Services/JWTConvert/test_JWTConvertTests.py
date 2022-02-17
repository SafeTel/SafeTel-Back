##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## JWTConvertTests
##

# Role import
from Logic.Models.Roles import Roles

# JWTConvert import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
import jwt

import os

def JWTConvert_ClassicUsage_Nominal():
    # Assign
    expectedGuid = "123456789"
    expectedRole = Roles.USER

    jwtConv = JWTConvert()

    # Act
    serializedJwt = jwtConv.Serialize(expectedGuid, expectedRole)
    deserializedJwt = jwt.decode(jwt=serializedJwt, key="secret", algorithms='HS256')

    resultGuid = deserializedJwt["guid"]
    resultRole = deserializedJwt["role"]

    # Assert
    assert resultGuid == expectedGuid
    assert resultRole == expectedRole

def JWTConvert_BadJWT_None():
    # Assign
    jwtConv = JWTConvert()

    # Act
    serializedJwt = jwtConv.Deserialize("notajwt")

    # Assert
    assert serializedJwt == None
