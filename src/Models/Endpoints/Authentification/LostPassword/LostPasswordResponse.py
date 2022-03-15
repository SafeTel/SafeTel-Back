##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## LostPassword.Response
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents LostPassword Response
class LostPasswordResponse(JParent):
    def __init__(self, emlailsent: bool):
        self.__InitJParent(emlailsent)

    # Values Assignement
    def __InitJParent(self, emlailsent: bool):
        self.emlailsent = emlailsent

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.emlailsent is None): return "Internal Model Error"
        if (type(self.emlailsent) is not bool): return "Internal Model Error"
        return None
