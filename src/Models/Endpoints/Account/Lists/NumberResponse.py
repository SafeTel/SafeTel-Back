##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## AddNumberResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Number Request
class NumberResponse(JParent):
    def __init__(self, Phonelist: list):
        self.__InitJParent(Phonelist)

    # Values Assignement
    def __InitJParent(self, Phonelist: list):
        self.Phonelist = Phonelist

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Phonelist is None): return "Internal server error"
        if (type(self.Phonelist) is not list): return "Internal server error"
        return None
