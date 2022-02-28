##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## DeleteAccount.Request
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents DeleteAccount Request
class DeleteAccountRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.userName = self.LoadElement(loadedJSON, "username")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token denied."
        if (self.userName is None): return "Body Denied"
        if (type(self.userName) is not str): return "Email denied."
        return None
