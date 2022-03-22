##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## AvaibleUpdateRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Avaible Update Request
class AvaibleUpdateRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.version = self.LoadElement(loadedJSON, "version")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.version is None): return "Body Denied"
        if (type(self.version) is not float): return "Invalid variable type"
        return None
