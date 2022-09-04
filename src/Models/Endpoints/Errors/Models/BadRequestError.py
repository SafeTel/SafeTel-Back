##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Bad Request
##

# Represent a RequestErrorManager Object
from Models.Endpoints.Errors.Models.EObject import EObject

class BadRequestError(EObject):
    def __init__(self, loadedJSON: dict):
        super().__init__(loadedJSON)
