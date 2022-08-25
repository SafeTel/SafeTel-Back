##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ErrorManager
##


### INFRA
# Endpoints import

# Represent a ErrorManager Object
from Models.Endpoints.Errors.Models.BadRequestError import BadRequestError
from Models.Endpoints.Errors.Models.ForbiddenAccessError import ForbiddenAccessError
from Models.Endpoints.Errors.Models.InternalLogicError import InternalLogicError
from Models.Endpoints.Errors.Models.ProxyAuthenticationRequiredError import ProxyAuthenticationRequiredError


class ErrorFactory():
    def BadRequestError(self, ErrorJson):
        return BadRequestError(ErrorJson)

    def InternalLogicError(self, ErrorJson):
        return InternalLogicError(ErrorJson)

    def ForbiddenAccessError(self, ErrorJson):
        return ForbiddenAccessError(ErrorJson)

    def ForbiddenAccessErrorWithMessage(self, ErrorJson):
        return ForbiddenAccessError(ErrorJson)

    def ProxyAuthenticationRequiredError(self, ErrorJson):
        return ProxyAuthenticationRequiredError(ErrorJson)