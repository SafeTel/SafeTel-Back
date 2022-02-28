##
## EPITECH PROJECT, 2022
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
