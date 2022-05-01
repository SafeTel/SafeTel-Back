##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EvaluateCallRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# HistoryCallRequest import
from Models.Endpoints.Account.Lists.History.HistoryCallRequest import HistoryCallRequest

# Represents Tellows Request
class EvaluateCallRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitCallJObject(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.boxid = self.LoadElement(loadedJSON, "boxid")
        self.report = self.LoadElement(loadedJSON, "report")

    def __InitCallJObject(self, loadedJSON: dict):
        callRaw = self.LoadElement(loadedJSON, "Call")
        self.Call = None if callRaw is None else HistoryCallRequest(callRaw)


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaCallJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"

        if (self.boxid is None): return "Body Denied"
        if (type(self.boxid) is not str): return "Box ID Denied"

        if (self.report is None): return "Body Denied"
        if (type(self.report) is not bool): return "Report Denied"
        return None

    def __EvaCallJObject(self):
        if (self.Call is None): return "Body Denied"
        errorJObject = self.Call.EvaluateModelErrors()
        if (errorJObject != None): return errorJObject
        return None
