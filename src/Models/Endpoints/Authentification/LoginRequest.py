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
        self.magicnumber = self.LoadElement(loadedJSON, "magicnumber")
        self.email = self.LoadElement(loadedJSON, "email")
        self.password = self.LoadElement(loadedJSON, "password")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.magicnumber is None): return "Body Denied"
        if (type(self.magicnumber) is not int and self.magicnumber != 42): return "Body Denied"
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Email Denied"
        if (self.password is None): return "Body Denied"
        if (type(self.password) is not str): return "Password Denied"
        return None
