##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateActivityRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Request
class UpdateActivityRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.boxid = self.LoadElement(loadedJSON, "boxid")
        self.activity = self.LoadElement(loadedJSON, "activity")

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

        if (self.activity is None): return "Body Denied"
        if (type(self.activity) is not bool): return "Activity Denied"
        return None
