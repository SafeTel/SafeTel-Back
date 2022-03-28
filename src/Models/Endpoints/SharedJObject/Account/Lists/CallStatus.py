##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CallStatus
##

from dataclasses import MISSING
from enum import IntEnum

class CallStatus(IntEnum):
    MISSED = 1
    RECEIVED = 2
    BLOCKED = 3
    OUTGOING = 4


    @classmethod
    def HasValue(cls, value):
        return value in cls._value2member_map_


    @classmethod
    def StrToEnum(cls, s: str):
        if (s == None):
            return None
        if (s.lower() == "missed"):
            return CallStatus.MISSED
        elif (s.lower() == "received"):
            return CallStatus.RECEIVED
        elif (s.lower() == "blocked"):
            return CallStatus.BLOCKED
        elif (s.lower() == "outgoing"):
            return CallStatus.OUTGOING
        return None


    @classmethod
    def EnumToStr(cls, value):
        if (value == CallStatus.MISSED):
            return "Missed"
        elif (value == CallStatus.RECEIVED):
            return "Received"
        elif (value == CallStatus.BLOCKED):
            return "Blocked"
        elif (value == CallStatus.OUTGOING):
            return "Outgoing"
        return None
