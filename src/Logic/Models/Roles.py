##
## EPITECH PROJECT, 2021
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
    def has_value(cls, value):
        return value in cls._value2member_map_
