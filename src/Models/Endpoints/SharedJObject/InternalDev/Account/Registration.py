##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Registration
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Shared JObject imports
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

class Registration(JObject):
    def __init__(self, loadedJSON):
        if (loadedJSON == None):
            return
        self.__InitCurrJObjectt(loadedJSON)
        self.__InitCustomerInfosJObject(loadedJSON)
        self.__InitLocalizationJObject(loadedJSON)

    # Values Assignement
    def __InitCurrJObjectt(self, loadedJSON: dict):
        self.username = self.LoadElement(loadedJSON, "username")
        self.email = self.LoadElement(loadedJSON, "email")
        self.password = self.LoadElement(loadedJSON, "password")

    def __InitCustomerInfosJObject(self, loadedJSON: dict):
        customerInfosRaw = self.LoadElement(loadedJSON, "CustomerInfos")
        self.CustomerInfos = None if customerInfosRaw is None else CustomerInfos(customerInfosRaw)

    def __InitLocalizationJObject(self, loadedJSON: dict):
        localizationRaw = self.LoadElement(loadedJSON, "Localization")
        self.Localization = None if localizationRaw is None else Localization(localizationRaw)

    # Errors Evaluation
    def EvaErrorsJObject(self):
        if (self.username is None): return "Body Denied"
        if (type(self.username) is not str): return "Invalid variable type."
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Invalid variable type."
        if (self.password is None): return "Body Denied"
        if (type(self.password) is not str): return "Invalid variable type."
        return None
