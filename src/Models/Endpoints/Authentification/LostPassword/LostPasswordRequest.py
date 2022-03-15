##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## LostPassword.Request
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents LostPassword Request
class LostPasswordRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.email = self.LoadElement(loadedJSON, "email")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Email Denied"
        return None
