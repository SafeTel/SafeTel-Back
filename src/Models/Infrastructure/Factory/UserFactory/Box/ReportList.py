##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ReportList
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Model Shared import
from Models.Logic.Shared.EmbeddedErrorReport import EmbeddedErrorReport

# Represents Number Request
class ReportList(JObject):
    def __init__(self, Reports: list):
        self.__InitJObject(Reports)


    # Values Assignement
    def __InitJObject(self, Reports: list):
        self.Reports = []
        for Rpt in Reports:
            tmp = EmbeddedErrorReport()
            self.Reports.append(
                tmp.InitValues(
                    Rpt["trace"],
                    Rpt["ts"],
                    Rpt["message"],
                    Rpt["type"]
            ))


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None


    def __EvaErrorsJParent(self):
        if (self.Boxes is None): return "Internal Model Error"
        if (type(self.Boxes) is not list): return "Internal Model Error"
        return None


    def __EvaErrorsJObject(self):
        for Box in self.Reports:
            errorJObject = self.__EvaErrorReport(Box)
            if (errorJObject != None):
                return errorJObject
        return None


    def __EvaErrorReport(self, Reports: EmbeddedErrorReport):
        errorBox = Reports.EvaluateModelErrors()
        return errorBox

