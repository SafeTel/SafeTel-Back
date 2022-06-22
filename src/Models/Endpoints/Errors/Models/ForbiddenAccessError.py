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
        self.__LogingError()

    def __LogingError(self):
        ## TODO: waiting for logging class
        return
