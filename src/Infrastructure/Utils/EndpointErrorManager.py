##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EndpointErrorManager
##

class EndpointErrorManager():
    # Code 400
    def CreateBadRequestError(self, details):
        return {
            "error": True,
            "detail": details
        }

    # Code 500
    def CreateInternalLogicError(self):
        return {
            "error": True,
            "details": "Internal Logic Error",
            "message": "Contact SafeTel Backend devs"
        }

    # Code 403
    def CreateForbiddenAccessError(self):
        return {
            "error": True,
            "details": "Access Denied",
            "message": "Your token may be corrupted"
        }
