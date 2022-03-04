##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## HistoryResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Model shared import
from Models.Endpoints.SharedJObject.Account.Lists.HistoryCall import HistoryCall

# Represents Number Request
class HistoryResponse(JParent):
    def __init__(self, History: list):
        self.__InitJParent(History)

    # Values Assignement
    def __InitJParent(self, History: list):
        self.History = []
        for historyCall in History:
            self.History.append(
                HistoryCall(
                    historyCall["number"],
                    historyCall["status"],
                    historyCall["time"]
            ))

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.History is None): return "Internal Model Error"
        if (type(self.History) is not list): return "Internal Model Error"
        return None
