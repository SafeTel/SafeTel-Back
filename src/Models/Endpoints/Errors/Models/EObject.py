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
        self.Details = self.LoadElement(loadedJSON, "details")
        self.Message = self.LoadElement(loadedJSON, "message")
        self.WithMessage = True if self.Message is not None else False

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorEObject = self.__EvaErrorsEObject()
        if (errorEObject != None): return errorEObject
        return None

    def __EvaErrorsEObject(self):
        if (self.Details is None): return "Internal Model Error - Model missing element - $details"
        if (type(self.Details) is not str): return "Internal Model Error - Invalid variable type - $details"
        if (self.Details is ""): return "Internal Model Error - Element empty - $details"

        if (self.WithMessage is False): return None

        if (self.Message is None): return "Internal Model Error - Model missing element - $message"
        if (type(self.Message) is not str): return "Internal Model Error - Invalid variable type - $message"
        if (self.Message is ""): return "Internal Model Error - Element empty - $message"

        return None
