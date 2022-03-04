##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## WhitelistResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Whitelist Response
class WhitelistResponse(JParent):
    def __init__(self, Whitelist: list):
        self.__InitJParent(Whitelist)

    # Values Assignement
    def __InitJParent(self, Whitelist: list):
        self.Whitelist = Whitelist

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Whitelist is None): return "Internal server error"
        if (type(self.Whitelist) is not list): return "Internal server error"
        return None
