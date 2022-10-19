##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetReportedNumbersResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent


# Represents Reported Count Response
class GetReportedNumbersResponse(JParent):
    def __init__(self, Numbers: int):
        self.__InitJParent(Numbers)

    # Values Assignement
    def __InitJParent(self, Numbers: int):
        self.Numbers = Numbers

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Numbers is None): return "Internal Model Error"
        if (type(self.Numbers) is not list): return "Internal Model Error"
        return None
