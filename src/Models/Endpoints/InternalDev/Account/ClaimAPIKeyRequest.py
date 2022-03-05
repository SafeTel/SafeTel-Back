##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ClaimAPIKeyRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Claim API Key Request
class ClaimAPIKeyRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)


    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.magicnumber = self.LoadElement(loadedJSON, "magicnumber")
        self.name = self.LoadElement(loadedJSON, "name")


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None


    def __EvaErrorsJParent(self):
        if (self.magicnumber is None): return "Body Denied"
        if (type(self.magicnumber) is not int and self.magicnumber != 42): return "Body Denied"
        if (self.name is None): return "Body Denied"
        if (type(self.name) is not str): return "Name Denied"
        return None
