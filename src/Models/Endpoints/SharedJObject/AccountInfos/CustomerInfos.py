##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## CustomerInfos
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject

# Reprensents CustomerInfos
class CustomerInfos(JObject):
    def __init__(self, loadedJSON: dict):
        if (loadedJSON == None):
            return
        self.__InitJObjectt(loadedJSON)

    # Values Assignement
    def __InitJObjectt(self, loadedJSON: dict):
        self.firstName = self.LoadElement(loadedJSON, "firstName")
        self.lastName = self.LoadElement(loadedJSON, "lastName")
        self.phoneNumber = self.LoadElement(loadedJSON, "phoneNumber")

    # Errors Evaluation
    def EvaErrorsJObject(self):
        if (type(self.firstName) is not str): return "Invalid variable type."
        if (type(self.lastName) is not str): return "Invalid variable type."
        if (type(self.phoneNumber) is not str): return "Invalid variable type."
        return None
