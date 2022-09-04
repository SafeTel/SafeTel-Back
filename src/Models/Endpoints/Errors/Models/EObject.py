##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EObject
##

### LOGIC
# json reader import
import string

from Models.ModelAbstractions.JObject import JObject

# Represent an Error Object
class EObject(JObject):
    def __init__(self, loadedJSON: dict):
        self.__InitEObject(loadedJSON)

    # Values Assignement
    def __InitEObject(self, loadedJSON: dict):
        self.details = self.LoadElement(loadedJSON, "details")
        self.error = self.LoadElement(loadedJSON, "error")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorEObject = self.__EvaErrorsEObject()
        if (errorEObject != None): return errorEObject
        return None

    def __EvaErrorsEObject(self):
        if (self.details is None): return "Internal Model Error - Model missing element - $details"
        if (type(self.details) is not str): return "Internal Model Error - Invalid variable type - $details"
        if (self.details == ""): return "Internal Model Error - Element empty - $details"

        if (self.error is None): return "Internal Model Error - Model missing element - $error"
        if (type(self.error) is not bool): return "Internal Model Error - Invalid variable type - $error"


        return None
