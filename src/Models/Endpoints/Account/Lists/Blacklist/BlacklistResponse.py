##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## BlacklistResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Blacklist Response
class BlacklistResponse(JParent):
    def __init__(self, Blacklist: list):
        self.__InitJParent(Blacklist)

    # Values Assignement
    def __InitJParent(self, Blacklist: list):
        self.Blacklist = Blacklist

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Blacklist is None): return "Internal server error"
        if (type(self.Blacklist) is not list): return "Internal server error"
        return None
