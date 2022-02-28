##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CallOrigin
##

from enum import IntEnum

class CallStatus(IntEnum):
    MISSED = 1
    RECEIVED = 2
    BLOCKED = 3
    OUTGOING = 4

    @classmethod
    def HasValue(cls, value):
        return value in cls._value2member_map_
