##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateLostPasswordResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents LostPassword Response
class UpdateLostPasswordResponse(JParent):
    def __init__(self, passwordupdated: bool):
        self.__InitJParent(passwordupdated)

    # Values Assignement
    def __InitJParent(self, passwordupdated: bool):
        self.passwordupdated = passwordupdated

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.passwordupdated is None): return "Internal Model Error"
        if (type(self.passwordupdated) is not bool): return "Internal Model Error"
        return None
