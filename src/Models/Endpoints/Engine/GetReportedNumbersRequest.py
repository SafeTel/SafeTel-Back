##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetReportedNumbersRequest
##


### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent


# Represents Reported Count Request
class GetReportedNumbersRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.index = self.LoadElement(loadedJSON, "index")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        if (self.index is None): return "Index Denied"
        if (type(self.index) is not int): return "Index Denied"
        if (self.index < 0): return "Index Denied"
        return None
