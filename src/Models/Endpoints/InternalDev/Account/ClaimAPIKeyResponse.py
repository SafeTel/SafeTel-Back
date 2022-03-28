##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## ClaimAPIKeyResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class ClaimAPIKeyResponse(JParent):
    def __init__(self, apiKey: str):
        self.__InitJParent(apiKey)

    # Values Assignement
    def __InitJParent(self, apiKey: str):
        self.apiKey = apiKey
        self.message = "only one apikey is allowed for an contributor or ip"

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.apiKey is None): return "Internal Model Error"
        if (type(self.apiKey) is not str): return "Internal Model Error"
        return None