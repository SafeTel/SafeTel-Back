##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## UserInfos
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared JObject imports
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

# Represents UpdatePErsonalInfos Request
class UserInfos(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitCustomerInfosJObject(loadedJSON)
        self.__InitLocalizationJObject(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.email = self.LoadElement(loadedJSON, "email")
        self.username = self.LoadElement(loadedJSON, "username")
        self.password = self.LoadElement(loadedJSON, "password")
        self.time = self.LoadElement(loadedJSON, "time")
        self.guid = self.LoadElement(loadedJSON, "guid")

    def __InitCustomerInfosJObject(self, loadedJSON: dict):
        customerInfosRaw = self.LoadElement(loadedJSON, "customerInfos")
        self.CustomerInfos = None if customerInfosRaw is None else CustomerInfos(customerInfosRaw)

    def __InitLocalizationJObject(self, loadedJSON: dict):
        localizationRaw = self.LoadElement(loadedJSON, "localization")
        self.Localization = None if localizationRaw is None else Localization(localizationRaw)

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaCustomerInfosJObject()
        if (errorJObject != None): return errorJObject
        errorJObject = self.__EvaLocalizationJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaErrorsJParent(self):
        if (self.email is None): return ""
        if (type(self.email) is not str): return "Email Denied."
        if (self.username is None): return "Body Denied"
        if (type(self.username) is not str): return "Username Denied."
        if (self.password is None): return "Passwor Denied"
        if (type(self.password) is not str): return "Body Denied."
        if (self.time is None): return "Time Denied"
        if (type(self.time) is not float): return "Body Denied."
        if (self.guid is None): return "GUID Denied"
        if (type(self.guid) is not str): return "Body Denied."
        return None

    def __EvaCustomerInfosJObject(self):
        if (self.CustomerInfos is None): return "Body Denied."
        errorJObject = self.CustomerInfos.EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaLocalizationJObject(self):
        if (self.Localization is None): return "Body Denied."
        errorJObject = self.Localization.EvaErrorsJObject()
        if (errorJObject != None):return errorJObject
        return None
