##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Administrative
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject

# Reprensents Localization
class Administrative(JObject):
    def __init__(self, loadedJSON: dict):
        if (loadedJSON == None):
            return
        self.__InitJObjectt(loadedJSON)

    def __init__(self, passwordlost: bool = False):
        self.__InitJObjectt(passwordlost)

    # Values Assignement
    def __InitJObjectt(self, loadedJSON: dict):
        self.passwordlost = self.LoadElement(loadedJSON, "passwordlost")

    def __InitJObjectt(self, passwordlost: bool):
        self.passwordlost = passwordlost

    # Errors Evaluation
    def EvaErrorsJObject(self):
        if (self.passwordlost is None): return "Body denied"
        if (type(self.passwordlost) is not bool): return "Invalid variable type"
        return None
