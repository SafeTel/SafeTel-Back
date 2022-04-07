##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## EvaluateNumberResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Tellows Response
class EvaluateNumberResponse(JParent):
    def __init__(self, block: bool):
        self.__InitJParent(block)

    # Values Assignement
    def __InitJParent(self, block: bool):
        self.block = block

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.block is None): return "Internal Model Error"
        if (type(self.block) is not bool): return "Internal Model Error"
        return None
