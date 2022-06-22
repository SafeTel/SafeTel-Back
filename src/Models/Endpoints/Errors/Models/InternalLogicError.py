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
        self.__LogingError()

    def __LogingError(self):
        ## TODO: waiting for logging class
        return
