##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## LoginResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Response
class LoginResponse(JParent):
    def __init__(self, username: str, token: str):
        self.__InitJParent(username, token)

    # Values Assignement
    def __InitJParent(self, username: str, token: str):
        self.username = username
        self.token = token

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.username is None): return "Internal Model Error"
        if (type(self.username) is not str): return "Internal Model Error"
        if (self.token is None): return "Internal Model Error"
        if (type(self.token) is not str): return "Internal Model Error"
        return None
