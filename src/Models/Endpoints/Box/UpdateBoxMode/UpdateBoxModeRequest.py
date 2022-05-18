##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateBoxModeRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Box Severity Enum import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity

# Represents Login Request
class UpdateBoxModeRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.boxid = self.LoadElement(loadedJSON, "boxid")
        self.severity = BoxSeverity.StrToEnum(self.LoadElement(loadedJSON, "severity"))

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"

        if (self.boxid is None): return "Body Denied"
        if (type(self.boxid) is not str): return "Box ID Denied"

        if (self.severity is None): return "Body Denied"
        if (type(self.severity) is not BoxSeverity): return "Severity Denied"
        if (not BoxSeverity.HasValue(self.severity)): return "Severity Denied"
        return None
