##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EvaluateCallResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Tellows Response
class EvaluateCallResponse(JParent):
    def __init__(self, message: str):
        self.__InitJParent(message)

    # Values Assignement
    def __InitJParent(self, message: str):
        self.message = message

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.message is None): return "Internal Model Error"
        if (type(self.message) is not str): return "Internal Model Error"
        return None
