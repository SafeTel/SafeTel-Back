##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ReportErrorResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class ReportErrorResponse(JParent):
    def __init__(self, received: bool):
        self.__InitJParent(received)

    # Values Assignement
    def __InitJParent(self, received: bool):
        self.received = received

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.received is None): return "Internal Model Error"
        if (type(self.received) is not bool): return "Internal Model Error"

        return None
