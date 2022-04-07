##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## LoginBoxRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Request
class LoginBoxRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.boxid = self.LoadElement(loadedJSON, "boxid")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.boxid is None): return "Body Denied"
        if (type(self.boxid) is not str): return "Box ID Denied"
        return None
