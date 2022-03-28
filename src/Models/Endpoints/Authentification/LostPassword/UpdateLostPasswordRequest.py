##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateLostPassword
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents UpdateLostPassword Request
class UpdateLostPasswordRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.password = self.LoadElement(loadedJSON, "password")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        if (self.password is None): return "Body Denied"
        if (type(self.password) is not str): return "Password Denied"
        return None
