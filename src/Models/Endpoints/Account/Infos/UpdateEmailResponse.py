##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateEmail.Response
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class UpdateEmailResponse(JParent):
    def __init__(self, updated: bool):
        self.__InitJParent(updated)

    # Values Assignement
    def __InitJParent(self, updated: bool):
        self.updated = updated

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.updated is None): return "Internal Model Error"
        if (type(self.updated) is not bool): return "Internal Model Error"
        return None
