##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## AddHistoryRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Add History Request
class AddHistoryRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.number = self.LoadElement(loadedJSON, "number")
        self.status = self.LoadElement(loadedJSON, "status")
        self.time = self.LoadElement(loadedJSON, "time")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token denied."
        if (self.number is None): return "Body Denied"
        if (type(self.number) is not str): return "Token denied."
        if (self.status is None): return "Body Denied"
        if (type(self.status) is not str): return "Token denied."
        if (self.time is None): return "Body Denied"
        if (type(self.time) is not int): return "Token denied."
        return None
