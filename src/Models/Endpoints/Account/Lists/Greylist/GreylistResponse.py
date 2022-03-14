##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GreylistResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Number Request
class GreylistResponse(JParent):
    def __init__(self, Blacklist: list, Whitelist: list):
        self.__InitJParent(Blacklist, Whitelist)

    # Values Assignement
    def __InitJParent(self, Blacklist: list, Whitelist: list):
        self.Blacklist = Blacklist
        self.Whitelist = Whitelist

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Blacklist is None): return "Internal Model Error"
        if (type(self.Blacklist) is not list): return "Internal Model Error"
        if (self.Whitelist is None): return "Internal Model Error"
        if (type(self.Whitelist) is not list): return "Internal Model Error"
        return None
