##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## ClaimAPIKeyRequest
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared JObject import
from Models.Endpoints.SharedJObject.InternalDev.Account.Registration import Registration

# Represents Register Admin Dev Request
class RegisterAdminDevRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitJObject(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.magicnumber = self.LoadElement(loadedJSON, "magicnumber")
        self.apiKey = self.LoadElement(loadedJSON, "apiKey")
        self.role = self.LoadElement(loadedJSON, "role")

    def __InitJObject(self, loadedJSON: dict):
        registrationRaw = self.LoadElement(loadedJSON, "registration")
        self.Registrattion = None if registrationRaw is None else Registration(registrationRaw)

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaRegistrationJObject()
        if (errorJParent != None): return errorJObject
        return None

    def __EvaErrorsJParent(self):
        if (self.magicnumber is None): return "Body Denied"
        if (type(self.magicnumber) is not int and self.magicnumber != 42): return "Body Denied."
        if (self.apiKey is None): return "Body Denied."
        if (type(self.apiKey) is not str): return "Invalid variable type."
        if (self.role is None): return "Body Denied."
        if (type(self.role) is not str): return "Invalid variable type."
        return None

    def __EvaRegistrationJObject(self):
        if (self.CustomerInfos is None): return "Body Denied."
        errorJObject = self.CustomerInfos.EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None