##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ErrorManager
##


### INFRA
# Endpoints import
from Models.Endpoints.Errors.Factory.ErrorFactory import ErrorFactory

class ErrorManager():
    def __init__(self):
        self.__ErrorFactory = ErrorFactory()

    def BadRequestError(self, details):
        ErrorJson = {
            "error": True,
            "details": details
        }
        return self.__ErrorFactory.BadRequestError(ErrorJson)

    def InternalLogicError(self):
        ErrorJson = {
            "error": True,
            "details": "Internal Logic Error",
            "message": "Contact SafeTel Backend devs"
        }
        return self.__ErrorFactory.InternalLogicError(ErrorJson)

    def ForbiddenAccessError(self):
        ErrorJson = {
            "error": True,
            "details": "Access Denied",
            "message": "Your token may be corrupted"
        }
        return self.__ErrorFactory.ForbiddenAccessError(ErrorJson)

    def ForbiddenAccessErrorWithMessage(self, message):
        ErrorJson = {
            "error": True,
            "details": "Access Denied",
            "message": message
        }
        return self.__ErrorFactory.ForbiddenAccessErrorWithMessage(ErrorJson)

    # Code 407, error for IP of embedded
    def ProxyAuthenticationRequiredError(self):
        ErrorJson = {
            "error": True,
            "details": "IP Denied"
        }
        return self.__ErrorFactory.ProxyAuthenticationRequiredError(ErrorJson)
