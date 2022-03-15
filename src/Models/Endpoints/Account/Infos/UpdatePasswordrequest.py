##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## UpdatePasswordrequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents UpdatePErsonalInfos Request
class UpdatePasswordRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.oldpassword = self.LoadElement(loadedJSON, "oldpassword")
        self.newpassword = self.LoadElement(loadedJSON, "newpassword")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        if (self.oldpassword is None): return "Body Denied"
        if (type(self.oldpassword) is not str): return "Old Paswword Denied"
        if (self.newpassword is None): return "Body Denied"
        if (type(self.newpassword) is not str): return "New Paswword Denied"
        return None
