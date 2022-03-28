##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BoxSeverity
##

from dataclasses import MISSING
from enum import IntEnum

class BoxSeverity(IntEnum):
    NONE = 1
    BLACKLIST = 2
    NORMAL = 3
    HIGH = 4
    MAX = 5


    @classmethod
    def HasValue(cls, value):
        return value in cls._value2member_map_


    @classmethod
    def StrToEnum(cls, s: str):
        if (s == None):
            return None
        if (s.lower() == "none"):
            return BoxSeverity.NONE
        elif (s.lower() == "blacklist"):
            return BoxSeverity.BLACKLIST
        elif (s.lower() == "normal"):
            return BoxSeverity.NORMAL
        elif (s.lower() == "high"):
            return BoxSeverity.HIGH
        elif (s.lower() == "max"):
            return BoxSeverity.MAX
        return None


    @classmethod
    def EnumToStr(cls, value):
        if (value == BoxSeverity.NONE):
            return "None"
        elif (value == BoxSeverity.BLACKLIST):
            return "Blacklist"
        elif (value == BoxSeverity.NORMAL):
            return "Normal"
        elif (value == BoxSeverity.HIGH):
            return "High"
        elif (value == BoxSeverity.MAX):
            return "Max"
        return None
