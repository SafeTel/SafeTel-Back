##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## AddHistoryRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Sub JObject import
from Models.Endpoints.Account.Lists.History.HistoryCallRequest import HistoryCallRequest

# Represents Add History Request
class AddHistoryRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitJObject(loadedJSON)


    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")


    def __InitJObject(self, loadedJSON: dict):
        historyCallRaw = self.LoadElement(loadedJSON, "HistoryCall")
        self.HistoryCall = None if historyCallRaw is None else HistoryCallRequest(historyCallRaw)


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None


    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        return None


    def __EvaErrorsJObject(self):
        if (self.HistoryCall is None): return "Body Denied"
        errorJObject = self.HistoryCall.EvaluateModelErrors()
        if (errorJObject != None): return errorJObject
        return None
