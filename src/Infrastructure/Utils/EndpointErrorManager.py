##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## EndpointErrorManager
##

class EndpointErrorManager():
    def CreateBadRequestError(self, details):
        return {
            "error": True,
            "detail": details
        }

    def CreateInternalLogicError():
        return {
            "error": True,
            "details": "internal logic error"
        }
