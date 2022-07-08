##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Forbidden Access
##

# Represent a RequestErrorManager Object
from Models.Endpoints.Errors.Models.EObject import EObject

class ForbiddenAccessError(EObject):
    def __init__(self, loadedJSON: dict):
        super().__init__(loadedJSON)
        self.__InitForbiddenAccessError(loadedJSON)

    def __InitForbiddenAccessError(self, loadedJSON):
        self.message = self.LoadElement(loadedJSON, "message")

    def EvaluateModelErrors(self):
        errorEObject = self.__EvaErrorsForbiddenAccessError()
        if (errorEObject != None): return errorEObject
        return super().EvaluateModelErrors()

    def __EvaErrorsForbiddenAccessError(self):
        if (self.message is None): return "Internal Model Error - Model missing element - $message"
        if (type(self.message) is not str): return "Internal Model Error - Invalid variable type - $message"
        if (self.message == ""): return "Internal Model Error - Element empty - $message"

        return None
