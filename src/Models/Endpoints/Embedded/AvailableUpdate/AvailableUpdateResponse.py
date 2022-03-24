##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## AvaibleUpdateResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Available Update Response
class AvailableUpdateResponse(JParent):
    def __init__(self, update: bool):
        self.__InitJParent(update)

    # Values Assignement
    def __InitJParent(self, update: bool):
        self.update = update

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.update is None): return "Internal Model Error"
        if (type(self.update) is not bool): return "Internal Model Error"
        return None