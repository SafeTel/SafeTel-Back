##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryCall
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
from Models.ModelAbstractions.JParent import JParent
# Shared Enum import
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus

# Represents Number Request
class HistoryCallRequest(JObject):
    def __init__(self, loadedJSON: dict):
        self.__InitJObject(loadedJSON)


    # Values Assignement
    def __InitJObject(self, loadedJSON: dict):
        self.number = self.LoadElement(loadedJSON, "number")
        self.status = CallStatus.StrToEnum(self.LoadElement(loadedJSON, "status"))
        self.time = self.LoadElement(loadedJSON, "time")


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJObject()
        if (errorJParent != None): return errorJParent
        return None


    def __EvaErrorsJObject(self):
        if (self.number is None): return "Internal Model Error - Model missing element - $number"
        if (type(self.number) is not str): return "Internal Model Error - Invalid variable type"

        if (self.status is None): return "Internal Model Error - Model missing element - $status"
        if (not CallStatus.HasValue(self.status)): return "Internal Model Error - Invalid variable type"

        if (self.time is None): return "Internal Model Error - Model missing element - $time"
        if (type(self.time) is not int): return "Internal Model Error - Invalid variable type"
        return None
