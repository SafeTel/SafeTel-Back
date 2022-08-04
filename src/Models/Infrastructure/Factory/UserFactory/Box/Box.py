##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Box
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Shared Enum import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity
# List converter import
from Models.Infrastructure.Factory.UserFactory.Box.ReportList import ReportList

# Represents Number Request
class Box(JObject):
    def __init__(self, loadedJSON: dict):
        self.__InitInputJObject(loadedJSON)

    def __init__(self, boxid: str, call: bool, ip: str, activity: bool, severity: BoxSeverity, ReportsList: list):
        self.__InitOutputJObject(boxid, call, ip, activity, severity, ReportsList)

    # Values Assignement
    def __InitInputJObject(self, loadedJSON: dict):
        self.boxid = self.LoadElement(loadedJSON, "boxid")
        self.call = self.LoadElement(loadedJSON, "call")
        self.ip = self.LoadElement(loadedJSON, "ip")
        self.activity = self.LoadElement(loadedJSON, "activity")
        self.severity = BoxSeverity.StrToEnum(self.LoadElement(loadedJSON, "severity"))
        self.severity = ReportList(self.LoadElement(loadedJSON, "Reports"))


    def __InitOutputJObject(self, boxid: str, call: bool, ip :str, activity: bool, severity: BoxSeverity, ReportsList: list):
        self.boxid = boxid
        self.call = call
        self.ip = ip
        self.activity = activity
        self.severity = severity
        self.Reports = ReportsList


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJObject()
        if (errorJParent != None): return errorJParent
        return None


    def __EvaErrorsJObject(self):
        if (self.boxid is None): return "Model missing element - $boxid"
        if (type(self.boxid) is not str): return "Invalid variable type - $boxid"

        if (self.call is None): return "Model missing element - $call"
        if (type(self.call) is not bool): return "Invalid variable type - $call"

        if (self.ip is None): return "Model missing element - $ip"
        if (type(self.ip) is not str): return "Invalid variable type - $ip"

        if (self.activity is None): return "Model missing element - $activity"
        if (type(self.activity) is not bool): return "Invalid variable type - $activity"

        if (self.severity is None): return "Model missing element - $severity"
        if (not BoxSeverity.HasValue(self.severity)): return "Invalid variable type - $severity"
        return None

