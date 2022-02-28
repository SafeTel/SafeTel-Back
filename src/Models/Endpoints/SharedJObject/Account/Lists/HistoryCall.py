##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryCall
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Shared JObject import
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus

# Represents Number Request
class HistoryCall(JObject):
    def __init__(self, number: str, status: CallStatus, time: int):
        self.__InitJParent(number, status, time)

    # Values Assignement
    def __InitJParent(self, number: str, status: CallStatus, time: int):
        self.number = number
        self.status = status
        self.time = time

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.number is None): return "Internal server error"
        if (type(self.number) is not str): return "Internal server error"
        if (self.status is None): return "Internal server error"
        if (not CallStatus.HasValue(self.status)): return "Internal server error"
        if (self.time is None): return "Internal server error"
        if (type(self.time) is not int): return "Internal server error"
        return None
