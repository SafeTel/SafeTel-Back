##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Proxy Authentication Required
##

# Represent a RequestErrorManager Object
from Models.Endpoints.Errors.Models.EObject import EObject

class ProxyAuthenticationRequiredError(EObject):
    def __init__(self, loadedJSON: dict):
        super().__init__(loadedJSON)
