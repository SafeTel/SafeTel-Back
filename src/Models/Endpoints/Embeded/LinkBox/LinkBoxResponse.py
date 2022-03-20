##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## LinkBoxResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Response
class LinkBoxResponse(JParent):
    def __init__(self, linked: bool):
        self.__InitJParent(linked)

    # Values Assignement
    def __InitJParent(self, linked: bool):
        self.linked = linked

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.linked is None): return "Internal Model Error"
        if (type(self.linked) is not bool): return "Internal Model Error"
        return None
