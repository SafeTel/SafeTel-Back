##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ErrorManagerFactory
##


### INFRA
# Endpoints import

# Represent a ErrorManagerFactory Object
from Models.Endpoints.Errors.Models.BadRequestError import BadRequestError
from Models.Endpoints.Errors.Models.ForbiddenAccessError import ForbiddenAccessError
from Models.Endpoints.Errors.Models.InternalLogicError import InternalLogicError


class ErrorManagerFactory():
    def BadRequestError(self, details):
        ErrorJson = {
            "error": True,
            "details": details
        }
        return BadRequestError(ErrorJson)

    def InternalLogicError(self):
        ErrorJson = {
            "error": True,
            "details": "Internal Logic Error",
            "message": "Contact SafeTel Backend devs"
        }
        return InternalLogicError(ErrorJson)

    def ForbiddenAccessError(self):
        ErrorJson = {
            "error": True,
            "details": "Access Denied",
            "message": "Your token may be corrupted"
        }
        return ForbiddenAccessError(ErrorJson)

    def ForbiddenAccessErrorWithMessage(self, message):
        ErrorJson = {
            "error": True,
            "details": "Access Denied",
            "message": message
        }
        return ForbiddenAccessError(ErrorJson)
