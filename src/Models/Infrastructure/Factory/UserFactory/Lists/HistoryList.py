##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryList
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Model Shared import
from Models.Endpoints.SharedJObject.Account.Lists.HistoryCall import HistoryCall
# Shared Enum import
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus

# Represents Number Request
class HistoryList(JObject):
    def __init__(self, History: list):
        self.__InitJObject(History)


    # Values Assignement
    def __InitJObject(self, History: list):
        self.History = []
        for HCall in History:
            self.History.append(
                HistoryCall(
                    HCall["number"],
                    CallStatus.StrToEnum(HCall["status"]),
                    HCall["time"]
            ))


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None


    def __EvaErrorsJParent(self):
        if (self.History is None): return "Internal Model Error"
        if (type(self.History) is not list): return "Internal Model Error"
        return None


    def __EvaErrorsJObject(self):
        for HCall in self.History:
            errorJObject = self.__EvaErrorHistoryCall(HCall)
            if (errorJObject != None):
                return errorJObject
        return None


    def __EvaErrorHistoryCall(self, HCall: HistoryCall):
        errorHistoryCall = HCall.EvaluateModelErrors()
        if (errorHistoryCall != None):
            return errorHistoryCall
        return None

