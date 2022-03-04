##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## PhoneList
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Number Request
class PhoneList(JParent):
    def __init__(self, PhoneNumbers: list):
        self.__InitJParent(PhoneNumbers)

    # Values Assignement
    def __InitJParent(self, PhoneNumbers: list):
        self.PhoneNumbers = PhoneNumbers

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.PhoneNumbers is None): return "Internal Model Error"
        if (type(self.PhoneNumbers) is not list): return "Internal Model Error"
        return None
