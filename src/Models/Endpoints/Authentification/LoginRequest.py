##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## LoginRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Login Request
class LoginRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.magicNumber = self.LoadElement(loadedJSON, "magicNumber")
        self.email = self.LoadElement(loadedJSON, "email")
        self.password = self.LoadElement(loadedJSON, "password")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.magicNumber is None): return "Body Denied"
        if (type(self.magicNumber) is not int and self.magicNumber != 42): return "Body denied."
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Email Denied."
        if (self.password is None): return "Body Denied"
        if (type(self.password) is not str): return "Password Denied."
        return None
