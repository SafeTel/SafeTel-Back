##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Model Shared import
from Models.Endpoints.SharedJObject.Account.Lists.HistoryCall import HistoryCall
# Model HistoryList Shared import
from Models.Infrastructure.Factory.UserFactory.Lists.HistoryList import HistoryList
# Enum import
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus

# Represents Number Request
class HistoryResponse(JParent):
    def __init__(self, History: list):
        self.__InitJParent(History)


    # Values Assignement
    def __InitJParent(self, History: list):
        self.History = []
        for HCall in History:
            self.History.append(
                self.__CreateHCbasic(HCall)
            )


    def __CreateHCbasic(self, HCall: HistoryCall):
        return {
            "number": HCall.number,
            "status": CallStatus.EnumToStr(HCall.status),
            "time": HCall.time
        }


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None


    def __EvaErrorsJParent(self):
        if (self.History is None): return "Internal Model Error"
        if (type(self.History) is not list): return "Internal Model Error"
        return None
