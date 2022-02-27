##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Localization
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject

# Reprensents Localization
class Localization(JObject):
    def __init__(self, loadedJSON: dict):
        if (loadedJSON == None):
            return
        self.__InitJObjectt(loadedJSON)

    # Values Assignement
    def __InitJObjectt(self, loadedJSON: dict):
        self.country = self.LoadElement(loadedJSON, "country")
        self.region = self.LoadElement(loadedJSON, "region")
        self.address = self.LoadElement(loadedJSON, "adress")

    # Errors Evaluation
    def EvaErrorsJObject(self):
        if (type(self.country) is not str): return "Invalid variable type."
        if (type(self.region) is not str): return "Invalid variable type."
        if (type(self.address) is not str): return "Invalid variable type."
        return None
