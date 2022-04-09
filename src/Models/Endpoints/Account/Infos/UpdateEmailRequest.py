##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateEmail.Request
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents UpdatePErsonalInfos Request
class UpdateEmailRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")
        self.email = self.LoadElement(loadedJSON, "email")

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Email Denied"
        return None
