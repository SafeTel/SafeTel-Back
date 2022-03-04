##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CheckTokenResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Check Token Request
class CheckTokenResponse(JParent):
    def __init__(self, validity: bool):
        self.__InitJParent(validity)

    # Values Assignement
    def __InitJParent(self, validity: bool):
        self.validity = validity

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.validity is None): return "Internal Model Error"
        if (type(self.validity) is not bool): return "Internal Model Error"
        return None
