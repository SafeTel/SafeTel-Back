##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Registration
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject

class Registration(JObject):
    def __init__(self, loadedJSON):
        if (loadedJSON == None):
            return
        self.__InitCurrJObjectt(loadedJSON)

    # Values Assignement
    def __InitCurrJObjectt(self, loadedJSON: dict):
        self.username = self.LoadElement(loadedJSON, "username")
        self.email = self.LoadElement(loadedJSON, "email")
        self.password = self.LoadElement(loadedJSON, "password")

    # Errors Evaluation
    def EvaErrorsJObject(self):
        if (self.username is None): return "Body Denied"
        if (type(self.username) is not str): return "Invalid variable type."
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Invalid variable type."
        if (self.password is None): return "Body Denied"
        if (type(self.password) is not str): return "Invalid variable type."
        return None
