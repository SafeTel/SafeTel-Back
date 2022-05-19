##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ResetEmbeddedTokenResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Reset Token Response
class ResetEmbeddedTokenResponse(JParent):
    def __init__(self, token: str):
        self.__InitJParent(token)

    # Values Assignement
    def __InitJParent(self, token: str):
        self.token = token

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Internal Model Error"
        if (type(self.token) is not str): return "Internal Model Error"
        return None
