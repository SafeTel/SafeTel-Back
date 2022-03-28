##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## RegisterResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class RegisterResponse(JParent):
    def __init__(self, created: bool, username: str, token: str):
        self.__InitJParent(created, username, token)

    # Values Assignement
    def __InitJParent(self, created: bool, username: str, token: str):
        self.created = created
        self.username = username
        self.token = token

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.created is None): return "Internal Model Error"
        if (type(self.created) is not bool): return "Internal Model Error"

        if (self.username is None): return "Internal Model Error"
        if (type(self.username) is not str): return "Internal Model Error"

        if (self.token is None): return "Internal Model Error"
        if (type(self.token) is not str): return "Internal Model Error"
        return None
