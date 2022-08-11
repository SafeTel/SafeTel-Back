##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ReportErrorRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared JObject imports
from Models.Logic.Shared.EmbeddedErrorReport import EmbeddedErrorReport

# Represents UpdatePErsonalInfos Request
class ReportErrorRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitEmbeddedErrorReport(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")

    def __InitEmbeddedErrorReport(self, loadedJSON: dict):
        EmbeddedErrorReportRaw = self.LoadElement(loadedJSON, "Error")
        self.Error = EmbeddedErrorReport()
        if (EmbeddedErrorReportRaw is None):
            self.Error = None
        else:
            self.Error.InitRawJSON(EmbeddedErrorReportRaw)

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaEmbeddedErrorReportJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        return None

    def __EvaEmbeddedErrorReportJObject(self):
        if (self.Error is None): return "Body Denied"
        errorJObject = self.Error.EvaluateModelErrors()
        if (errorJObject != None): return errorJObject
        return None
