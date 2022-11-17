##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ReportedCountResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent


# Represents Reported Count Response
class ReportedCountResponse(JParent):
    def __init__(self, count: int):
        self.__InitJParent(count)

    # Values Assignement
    def __InitJParent(self, count: int):
        self.count = count

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.count is None): return "Internal Model Error"
        if (type(self.count) is not int): return "Internal Model Error"
        return None

