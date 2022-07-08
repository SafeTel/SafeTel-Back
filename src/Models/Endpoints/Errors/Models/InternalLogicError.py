##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InternalLogic
##

# Represent a RequestErrorManager Object
from Models.Endpoints.Errors.Models.EObject import EObject

class InternalLogicError(EObject):
    def __init__(self, loadedJSON: dict):
        super().__init__(loadedJSON)
        self.__InitInternalLogicError(loadedJSON)

    def __InitInternalLogicError(self, loadedJSON):
        self.message = self.LoadElement(loadedJSON, "message")

    def EvaluateModelErrors(self):
        errorEObject = self.__EvaErrorsInternalLogicError()
        if (errorEObject != None): return errorEObject
        return super().EvaluateModelErrors()

    def __EvaErrorsInternalLogicError(self):
        if (self.message is None): return "Internal Model Error - Model missing element - $message"
        if (type(self.message) is not str): return "Internal Model Error - Invalid variable type - $message"
        if (self.message == ""): return "Internal Model Error - Element empty - $message"

        return None
