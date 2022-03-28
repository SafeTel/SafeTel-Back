##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## TellowsRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Tellows Request
class TellowsRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.magicnumber = self.LoadElement(loadedJSON, "magicnumber")
        self.number = self.LoadElement(loadedJSON, "number")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.magicnumber is None): return "Body Denied"
        if (type(self.magicnumber) is not int and self.magicnumber != 42): return "Token Denied"

        if (self.number is None): return "Body Denied"
        if (type(self.number) is not str): return "Token Denied"
        return None
