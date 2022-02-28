##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## LoginResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Response
class LoginResponse(JParent):
    def __init__(self, userName: str, token: str):
        self.__InitJParent(userName, token)

    # Values Assignement
    def __InitJParent(self, userName: str, token: str):
        self.userName = userName
        self.token = token

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.userName is None): return "Internal server error"
        if (type(self.userName) is not str): return "Internal server error"
        if (self.token is None): return "Internal server error"
        if (type(self.token) is not str): return "Internal server error"
        return None
