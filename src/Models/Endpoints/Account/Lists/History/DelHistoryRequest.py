##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## DelHistoryRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Delete History Request
class DelHistoryRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.number = self.LoadElement(loadedJSON, "number")
        self.time = self.LoadElement(loadedJSON, "time")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        if (self.number is None): return "Body Denied"
        if (type(self.number) is not str): return "Token Denied"
        if (self.time is None): return "Body Denied"
        if (type(self.time) is not int): return "Token Denied"
        return None

