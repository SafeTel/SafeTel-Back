##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Roles
##

from enum import IntEnum

class Roles(IntEnum):
    ADMIN = 1
    DEVELOPER = 2
    USER = 3

    @classmethod
    def HasValue(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def StrToEnum(cls, s: str):
        if (s.lower() == "admin"):
            return Roles.ADMIN
        elif (s.lower() == "developer"):
            return Roles.DEVELOPER
        elif (s.lower() == "user"):
            return Roles.USER
        return None

    @classmethod
    def EnumToStr(cls, value):
        if (value == Roles.ADMIN):
            return "Admin"
        elif (value == Roles.DEVELOPER):
            return "Developer"
        elif (value == Roles.USER):
            return "User"
        return None
