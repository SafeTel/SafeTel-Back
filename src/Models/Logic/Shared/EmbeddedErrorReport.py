##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EmbeddedErrorReport
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents DeleteAccount Request
class EmbeddedErrorReport(JParent):
    def InitValues(self, trace: str, ts: int, message: str, type: str):
        self.__InitOutputJObject(trace, ts, message, type)

    def InitRawJSON(self, loadedJSON: dict):
        self.__InitInputJObject(loadedJSON)

    # Values Assignement
    def __InitInputJObject(self, loadedJSON: dict):
        self.trace = self.LoadElement(loadedJSON, "trace")
        self.ts = self.LoadElement(loadedJSON, "ts")
        self.message = self.LoadElement(loadedJSON, "message")
        self.type = self.LoadElement(loadedJSON, "type")


    def __InitOutputJObject(self, trace: str, ts: int, message: str, type: str):
        self.trace = trace
        self.ts = ts
        self.message = message
        self.type = type


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.trace is None): return "Body Denied"
        if (type(self.trace) is not str): return "Trace Denied"

        if (self.ts is None): return "Body Denied"
        if (type(self.ts) is not int): return "TS Denied"

        if (self.message is None): return "Body Denied"
        if (type(self.message) is not str): return "Message Denied"

        if (self.type is None): return "Body Denied"
        if (type(self.type) is not str): return "Type Denied"
        return None
